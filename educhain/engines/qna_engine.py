# educhain/engines/qna_engine.py

from typing import Optional, Type, Any, List, Literal, Union, Tuple, Dict
from pydantic import BaseModel, Field, ValidationError
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from datetime import datetime
import concurrent.futures
import json
from pathlib import Path
from tqdm import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, RetrievalQA, LLMMathChain
from langchain.output_parsers import PydanticOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.callbacks.manager import get_openai_callback
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re
from langchain_core.messages import SystemMessage
from langchain.schema import HumanMessage
from educhain.core.config import LLMConfig
from educhain.models.qna_models import (
    MCQList, ShortAnswerQuestionList, TrueFalseQuestionList,
    FillInBlankQuestionList, MCQListMath, Option ,SolvedDoubt, SpeechInstructions,
    VisualMCQList, VisualMCQ, BulkMCQ, BulkMCQList
)
from educhain.utils.loaders import PdfFileLoader, UrlLoader
from educhain.utils.output_formatter import OutputFormatter
import base64
import os
from PIL import Image
import io

import matplotlib.pyplot as plt
import pandas as pd
import dataframe_image as dfi
from IPython.display import display, HTML


import random

QuestionType = Literal["Multiple Choice", "Short Answer", "True/False", "Fill in the Blank"]
OutputFormatType = Literal["pdf", "csv"]

VISUAL_QUESTION_PROMPT_TEMPLATE = """Generate exactly {num} quantitative questions based on the topic: {topic}.
        Each question should require a visual representation of the data (bar graph, pie chart, line graph, or scatter plot or table) along with a detailed instruction on how to create that visual and options for the question. The question should be solvable based on the data in the visual.

        The visual type should be chosen based on the topic.
        Here is the general guidance for the visualization type:
        - Use pie chart when visualizing proportions or parts of a whole.
        - Use bar or column chart for comparing discrete categories or for displaying the frequency distribution.
        - Use line graph for displaying changes over time or continuous data or relationship between two continuous variables.
        - Use scatter plot for showing the relationship between two continuous variables, to identify any patterns and cluster of data.
        - Use table when presenting exact numerical data in organized rows and columns.

        The graph instruction MUST have the following structure in JSON format, selecting the relevant keys based on the visual type:
        {{
            "type": "bar" or "pie" or "line" or "scatter" or "table",
            "x_labels": ["label 1", "label 2", "label 3", "label 4"] for bar or line graphs,
            "x_values": [value 1, value 2, value 3, value 4] for scatter plot,
            "y_values": [value 1, value 2, value 3, value 4] for bar or line graphs,
            "labels": ["label 1", "label 2", "label 3", "label 4"] for pie chart,
            "sizes": [value 1, value 2, value 3, value 4] for pie chart,
            "y_label": "label for the y axis" for bar, line, scatter,
            "title": "title of the graph or table",
           "labels" : [ "label 1", "label 2", "label 3" ] for multiple lines in line graphs,
           "data": [
                    {{ "column1": "value1", "column2": "value2", ... }},
                    {{ "column1": "value3", "column2": "value4", ... }},
                    ...
                   ] for table
        }}

        Output the response in JSON format with the following structure:
        {{
          "questions" : [
            {{
                "question": "question text",
                "options": ["option a","option b", "option c", "option d"],
                "graph_instruction": {{"type": "bar" or "pie" or "line" or "scatter" or "table", ...}},
                "answer": "Correct answer of the question",
                "explanation": "Explanation of the question"
            }},
              {{
                "question": "question text",
                "options": ["option a","option b", "option c", "option d"],
                "graph_instruction": {{"type": "bar" or "pie" or "line" or "scatter" or "table", ...}},
                "answer": "Correct answer of the question",
                "explanation": "Explanation of the question"
            }}
           ]
        }}
"""


class QnAEngine:
    def __init__(self, llm_config: Optional[LLMConfig] = None):
        if llm_config is None:
            llm_config = LLMConfig()
        self.llm = self._initialize_llm(llm_config)
        self.pdf_loader = PdfFileLoader()
        self.url_loader = UrlLoader()
        self.embeddings = None

    def _initialize_llm(self, llm_config: LLMConfig):
        if llm_config.custom_model:
            return llm_config.custom_model
        else:
            return ChatOpenAI(
                model=llm_config.model_name,
                api_key=llm_config.api_key,
                max_tokens=llm_config.max_tokens,
                temperature=llm_config.temperature,
                base_url=llm_config.base_url,
                default_headers=llm_config.default_headers
            )

    def _get_parser_and_model(self, question_type: QuestionType, response_model: Optional[Type[Any]] = None):
        if response_model:
            return PydanticOutputParser(pydantic_object=response_model), response_model
        if question_type == "Multiple Choice":
            return PydanticOutputParser(pydantic_object=MCQList), MCQList
        elif question_type == "Short Answer":
            return PydanticOutputParser(pydantic_object=ShortAnswerQuestionList), ShortAnswerQuestionList
        elif question_type == "True/False":
            return PydanticOutputParser(pydantic_object=TrueFalseQuestionList), TrueFalseQuestionList
        elif question_type == "Fill in the Blank":
            return PydanticOutputParser(pydantic_object=FillInBlankQuestionList), FillInBlankQuestionList
        elif response_model == VisualMCQList:
            return PydanticOutputParser(pydantic_object=VisualMCQList), VisualMCQList
        else:
            raise ValueError(f"Unsupported question type or response model: {question_type}, {response_model}")


    def _get_prompt_template(self, question_type: QuestionType, custom_template: Optional[str] = None):
        if custom_template == "graph":
            return VISUAL_QUESTION_PROMPT_TEMPLATE
        elif custom_template:
            return custom_template
        else:
            base_template = f"""
            Generate {{num}} {question_type} question(s) based on the given topic.
            Topic: {{topic}}

            For each question, provide:
            1. The question
            2. The correct answer
            3. An explanation (optional)
            """

            if question_type == "Multiple Choice":
                base_template += "\n4. A list of options (including the correct answer)"
            elif question_type == "Short Answer":
                base_template += "\n4. A list of relevant keywords"
            elif question_type == "True/False":
                base_template += "\n4. The correct answer as a boolean (true/false)"
            elif question_type == "Fill in the Blank":
                base_template += "\n4. The word or phrase to be filled in the blank"

            return base_template


    def _create_vector_store(self, content: str) -> Chroma:
        if self.embeddings is None:
            self.embeddings = OpenAIEmbeddings()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(content)

        vectorstore = Chroma.from_texts(texts, self.embeddings)

        return vectorstore

    def _setup_retrieval_qa(self, vector_store: Chroma) -> RetrievalQA:
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
        )

    def _load_data(self, source: str, source_type: str) -> str:
        if source_type == 'pdf':
            return self.pdf_loader.load_data(source)
        elif source_type == 'url':
            return self.url_loader.load_data(source)
        elif source_type == 'text':
            return source
        else:
            raise ValueError("Unsupported source type. Please use 'pdf', 'url', or 'text'.")

    def _handle_output_format(self, data: Any, output_format: Optional[OutputFormatType]) -> Union[Any, Tuple[Any, str]]:
        if output_format is None:
            return data

        formatter = OutputFormatter()
        if output_format == "pdf":
            output_file = formatter.to_pdf(data)
        elif output_format == "csv":
            output_file = formatter.to_csv(data)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        return data, output_file


    def _generate_and_save_visual(self, instruction, question_text, options, correct_answer):
        try:
            plt.figure(figsize=(10, 8))
            img_buffer = io.BytesIO()

            if instruction["type"] == "bar":
                plt.bar(instruction["x_labels"], instruction["y_values"], color="skyblue")
                plt.xlabel("Categories", fontsize=12)
                plt.ylabel(instruction["y_label"], fontsize=12)
                plt.title(instruction["title"], fontsize=14)
                plt.grid(axis="y", linestyle="--", alpha=0.7)
                plt.tight_layout()
                plt.savefig(img_buffer, format="png")

            elif instruction["type"] == "line":
                if isinstance(instruction["y_values"][0], list):
                    for i, y_vals in enumerate(instruction["y_values"]):
                        plt.plot(instruction["x_labels"], y_vals, marker="o", linestyle="-", label=instruction["labels"][i])
                else:
                    plt.plot(instruction["x_labels"], instruction["y_values"], marker="o", linestyle="-", color="b")

                plt.xlabel("X-axis", fontsize=12)
                plt.ylabel(instruction["y_label"], fontsize=12)
                plt.title(instruction["title"], fontsize=14)
                plt.grid(axis="y", linestyle="--", alpha=0.7)
                plt.legend()
                plt.tight_layout()
                plt.savefig(img_buffer, format="png")

            elif instruction["type"] == "pie":
                plt.pie(
                    instruction["sizes"],
                    labels=instruction["labels"],
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=plt.cm.Paired.colors
                )
                plt.title(instruction["title"], fontsize=14)
                plt.tight_layout()
                plt.savefig(img_buffer, format="png")

            elif instruction["type"] == "scatter":
                plt.scatter(instruction["x_values"], instruction["y_values"], color="r", alpha=0.7)
                plt.xlabel("X-axis", fontsize=12)
                plt.ylabel(instruction["y_label"], fontsize=12)
                plt.title(instruction["title"], fontsize=14)
                plt.grid(axis="both", linestyle="--", alpha=0.7)
                plt.tight_layout()
                plt.savefig(img_buffer, format="png")

            elif instruction["type"] == "table":
                df = pd.DataFrame(instruction["data"])
                img_buffer = io.BytesIO()
                dfi.export(df, img_buffer, table_conversion="matplotlib")

            plt.close()
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')

            if instruction["type"] != "table":
                display(HTML(f'<img src="data:image/png;base64,{img_base64}" style="max-width:500px; max-height:400px;">'))
            else:
                display(HTML(f'<img src="data:image/png;base64,{img_base64}" style="max-width:500px;">'))

            print("\nQuestion:", question_text)
            for idx, option in enumerate(options, start=1):
                print(f"{chr(64 + idx)}. {option}")
            print("Correct Answer:", correct_answer)
            print("-" * 80)

            return img_base64

        except Exception as e:
            print(f"Error generating visualization: {e}")
            return None


    def _display_visual_questions(self, ques: VisualMCQList):
        if ques and ques.questions:
            for q_data in ques.questions:
                instruction = q_data.graph_instruction
                question_text = q_data.question
                options = q_data.options
                correct_answer = q_data.answer

                self._generate_and_save_visual(instruction.dict(), question_text, options, correct_answer)
                print(q_data)
        else:
            print("Failed to generate visual questions or no questions were returned.")


    def generate_visual_questions(
        self,
        topic: str,
        num: int = 1,
        custom_instructions: Optional[str] = None,
        output_format: Optional[OutputFormatType] = None,
        **kwargs
    ) -> Optional[VisualMCQList]:
        parser, model = self._get_parser_and_model("Multiple Choice", VisualMCQList)
        format_instructions = parser.get_format_instructions()
        template = self._get_prompt_template("Multiple Choice", "graph")

        if custom_instructions:
            template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        template += "\n\nThe response should be in JSON format.\n{format_instructions}"

        question_prompt = PromptTemplate(
            input_variables=["num", "topic"],
            template=template,
            partial_variables={"format_instructions": format_instructions}
        )

        question_chain = question_prompt | self.llm
        results = question_chain.invoke(
            {"num": num, "topic": topic, **kwargs},
        )
        results = results.content

        try:
            structured_output = parser.parse(results)

            if output_format:
                self._handle_output_format(structured_output, output_format)

            if isinstance(structured_output, VisualMCQList):
                self._display_visual_questions(structured_output)

            return structured_output
        except Exception as e:
            print(f"Error parsing output in generate_visual_questions: {e}")
            print("Raw output:")
            print(results)
            return None


    def generate_questions(
        self,
        topic: str,
        num: int = 1,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        output_format: Optional[OutputFormatType] = None,
        **kwargs
    ) -> Any:
        parser, model = self._get_parser_and_model(question_type, response_model)
        format_instructions = parser.get_format_instructions()
        template = self._get_prompt_template(question_type, prompt_template)

        if custom_instructions:
            template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        template += "\n\nThe response should be in JSON format.\n{format_instructions}"

        question_prompt = PromptTemplate(
            input_variables=["num", "topic"],
            template=template,
            partial_variables={"format_instructions": format_instructions}
        )

        question_chain = question_prompt | self.llm
        results = question_chain.invoke(
            {"num": num, "topic": topic, **kwargs},
        )
        results = results.content

        try:
            structured_output = parser.parse(results)

            if output_format:
                self._handle_output_format(structured_output, output_format)


            return structured_output
        except Exception as e:
            print(f"Error parsing output in generate_questions: {e}")
            print("Raw output:")
            return model()


    def generate_questions_from_data(
        self,
        source: str,
        source_type: str,
        num: int,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        output_format: Optional[OutputFormatType] = None,
        **kwargs
    ) -> Any:
        content = self._load_data(source, source_type)
        return self.generate_questions(
            topic=content,
            num=num,
            question_type=question_type,
            prompt_template=prompt_template,
            custom_instructions=custom_instructions,
            response_model=response_model,
            output_format=output_format,
            **kwargs
        )

    def generate_questions_with_rag(
        self,
        source: str,
        source_type: str,
        num: int,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        learning_objective: str = "",
        difficulty_level: str = "",
        output_format: Optional[OutputFormatType] = None,
        **kwargs
    ) -> Any:
        if self.embeddings is None:
            self.embeddings = OpenAIEmbeddings()

        content = self._load_data(source, source_type)

        vector_store = self._create_vector_store(content)
        qa_chain = self._setup_retrieval_qa(vector_store)

        parser, model = self._get_parser_and_model(question_type, response_model)
        format_instructions = parser.get_format_instructions()

        template = self._get_prompt_template(question_type, prompt_template)


        prompt_template += """
        Learning Objective: {learning_objective}
        Difficulty Level: {difficulty_level}

        Ensure that the questions are relevant to the learning objective and match the specified difficulty level.

        The response should be in JSON format.
        {format_instructions}
        """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        question_prompt = PromptTemplate(
            input_variables=["num", "topic", "learning_objective", "difficulty_level"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        query = question_prompt.format(
            num=num,
            topic=content[:1000],
            learning_objective=learning_objective,
            difficulty_level=difficulty_level,
            **kwargs
        )

        results = qa_chain.invoke({"query": query, "n_results": 3})

        try:
            structured_output = parser.parse(results["result"])

            if output_format:
                self._handle_output_format(structured_output, output_format)


            return structured_output
        except Exception as e:
            print(f"Error parsing output in generate_questions_with_rag: {e}")
            print("Raw output:", results)
            return model()

    def generate_similar_options(self, question, correct_answer, num_options=3):
        llm = self.llm
        prompt = f"Generate {num_options} incorrect but plausible options similar to this correct answer: {correct_answer} for this question: {question}. Provide only the options, separated by semicolons. The options should not precede or end with any symbols, it should be similar to the correct answer."
        response = llm.predict(prompt)
        return response.split(';')

    def _validate_individual_question(self, question_dict: dict, question_model: Type[BaseModel] = None) -> Optional[BaseModel]:
        """
        Validate a single question and return None if validation fails.
        
        Args:
            question_dict: Dictionary containing question data
            question_model: Pydantic model class to validate against
        """
        try:
            if question_model is None:
                question_model = MCQList

            # Check for basic structure based on model fields
            required_fields = {field for field, _ in question_model.__fields__.items() 
                             if not question_model.__fields__[field].default_factory
                             and question_model.__fields__[field].default is None}
            
            if not all(field in question_dict for field in required_fields):
                missing = required_fields - set(question_dict.keys())
                print(f"Missing required fields: {missing}")
                return None

            # Validate through Pydantic model
            return question_model(**question_dict)
        except (ValidationError, KeyError, TypeError) as e:
            print(f"Validation error: {str(e)}")
            return None

    def _process_topics_data(self, topics_data):
        """Process topics data into a list of topic-subtopic-objective combinations"""
        combinations = []
        total_specified_questions = 0
        has_question_counts = False

        for topic in topics_data:
            for subtopic in topic["subtopics"]:
                for objective in subtopic["learning_objectives"]:
                    if isinstance(objective, dict) and "objective" in objective and "num_questions" in objective:
                        has_question_counts = True
                        combinations.append({
                            "topic": topic["topic"],
                            "subtopic": subtopic["name"],
                            "learning_objective": objective["objective"],
                            "num_questions": objective["num_questions"]
                        })
                        total_specified_questions += objective["num_questions"]
                    else:
                        # Handle the case where no question count is specified
                        objective_text = objective if isinstance(objective, str) else objective["objective"]
                        combinations.append({
                            "topic": topic["topic"],
                            "subtopic": subtopic["name"],
                            "learning_objective": objective_text,
                            "num_questions": None
                        })
        
        # Add the missing return statement
        return combinations, total_specified_questions, has_question_counts

    @retry(stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=4, max=10),
       retry=lambda e: isinstance(e, (ValidationError, json.JSONDecodeError)))
    def _generate_questions_with_retry(self, combo, num_questions, 
                                prompt_template=None, 
                                question_model=None,
                                question_list_model=None,
                                is_per_objective=False,
                                target_questions=None,
                                **kwargs):
        """
        Generate questions with improved retry mechanism and chunking
        """
        MAX_QUESTIONS_PER_BATCH = 3
        validated_questions = []
        remaining_questions = num_questions if not target_questions else target_questions
        total_attempts = 0
        max_attempts = max(5, (remaining_questions // MAX_QUESTIONS_PER_BATCH) * 2)

        while remaining_questions > 0 and len(validated_questions) < (target_questions or num_questions) and total_attempts < max_attempts:
            try:
                # Calculate batch size based on remaining questions
                current_batch_size = min(MAX_QUESTIONS_PER_BATCH, remaining_questions)
                
                # Generate the batch
                batch_questions = self.generate_questions(
                    topic=combo["topic"],
                    num=current_batch_size,
                    question_type="Multiple Choice",
                    prompt_template=prompt_template,
                    response_model=question_list_model,
                    subtopic=combo["subtopic"],
                    learning_objective=combo["learning_objective"],
                    **kwargs
                )

                # Process the batch
                if isinstance(batch_questions, question_list_model):
                    questions_to_validate = batch_questions.questions
                elif isinstance(batch_questions, dict) and 'questions' in batch_questions:
                    questions_to_validate = batch_questions.get('questions', [])
                else:
                    questions_to_validate = []
                    print(f"Unexpected response format: {type(batch_questions)}")

                # Validate questions
                for question in questions_to_validate:
                    if len(validated_questions) >= (target_questions or num_questions):
                        break

                    question_dict = question.dict() if hasattr(question, 'dict') else question
                    
                    if 'metadata' not in question_dict and hasattr(question_model, '__fields__') and 'metadata' in question_model.__fields__:
                        question_dict['metadata'] = {
                            "topic": combo["topic"],
                            "subtopic": combo["subtopic"],
                            "learning_objective": combo["learning_objective"]
                        }

                    validated_question = self._validate_individual_question(question_dict, question_model=question_model)
                    if validated_question:
                        validated_questions.append(validated_question)
                        remaining_questions -= 1

                total_attempts += 1

            except Exception as e:
                print(f"Error in generation attempt {total_attempts + 1}: {str(e)}")
                total_attempts += 1
                if not validated_questions:
                    continue

        return question_list_model(questions=validated_questions)

    def _process_math_result(self, math_result: Any) -> str:
        if isinstance(math_result, dict):
            if 'answer' in math_result:
                return math_result['answer'].split('Answer: ')[-1].strip()
            elif 'result' in math_result:
                return math_result['result'].strip()

        result_str = str(math_result)
        if 'Answer:' in result_str:
            return result_str.split('Answer:')[-1].strip()

        lines = result_str.split('\n')
        for line in reversed(lines):
            if line.strip().replace('.', '').isdigit():
                return line.strip()

        raise ValueError("Could not extract numerical result from LLMMathChain response")

    def generate_mcq_math(
        self,
        topic: str,
        num: int = 1,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        **kwargs
    ) -> Any:
        if response_model is None:
            parser = PydanticOutputParser(pydantic_object=MCQListMath)
        else:
            parser = PydanticOutputParser(pydantic_object=response_model)

        format_instructions = parser.get_format_instructions()

        template = self._get_prompt_template(question_type, prompt_template)


        prompt_template = """
            You are an Academic AI assistant specialized in generating multiple-choice math questions.
            Generate {num} multiple-choice questions (MCQ) based on the given topic.
            Each question MUST be a mathematical computation question.

            For each question:
            1. Make sure it requires mathematical calculation
            2. Set requires_math to true
            3. Provide clear numerical values
            4. Ensure the question has a single, unambiguous answer

            Topic: {topic}

            Format each question to include:
            - A clear mathematical problem
            - Four distinct numerical options
            - The correct answer
            - A step-by-step explanation
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\nThe response should be in JSON format.\n{format_instructions}"

        question_prompt = PromptTemplate(
            input_variables=["num", "topic"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        question_chain = question_prompt | self.llm
        results = question_chain.invoke(
            {"num": num, "topic": topic, **kwargs},
        )
        results = results.content

        try:
            structured_output = parser.parse(results)
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            return MCQListMath()

        llm_math = LLMMathChain.from_llm(llm=self.llm, verbose=True)

        for question in structured_output.questions:
            if question.requires_math:
                try:
                    math_result = llm_math.invoke({"question": question.question})

                    try:
                        solution = self._process_math_result(math_result)

                        numerical_solution = float(solution)
                        formatted_solution = f"{numerical_solution:.2f}"

                        question.explanation += f"\n\nMath solution: {formatted_solution}"

                        correct_option = Option(text=formatted_solution, correct='true')

                        variations = [0.9, 1.1, 1.2]
                        incorrect_options = []

                        for var in variations:
                            wrong_val = numerical_solution * var
                            incorrect_options.append(
                                Option(
                                    text=f"{wrong_val:.2f}",
                                    correct='false'
                                )
                            )

                        question.options = [correct_option] + incorrect_options
                        random.shuffle(question.options)

                    except (ValueError, TypeError) as e:
                        print(f"Error processing numerical result: {e}")
                        raise

                except Exception as e:
                    print(f"LLMMathChain failed to answer: {str(e)}")
                    question.explanation += "\n\nMath solution: Unable to compute."
                    question.options = [
                        Option(text="Unable to compute", correct='true'),
                        Option(text="N/A", correct='false'),
                        Option(text="N/A", correct='false'),
                        Option(text="N/A", correct='false')
                    ]

        return structured_output

    def _extract_video_id(self, url: str) -> str:
        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?:live\/)?(?:feature=player_embedded&v=)?(?:e\/)?(?:\/)?([^\s&amp;?#]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        raise ValueError("Invalid YouTube URL")

    def _get_youtube_transcript(self, video_id: str, target_language: str = 'en') -> tuple[str, str]:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            available_languages = [transcript.language_code for transcript in transcript_list]

            if not available_languages:
                raise ValueError("No transcripts available for this video")

            try:
                transcript = transcript_list.find_transcript([target_language])
                return TextFormatter().format_transcript(transcript.fetch()), target_language
            except:
                transcript = transcript_list.find_transcript(available_languages)
                original_language = transcript.language_code

                if transcript.is_translatable and target_language != original_language:
                    translated = transcript.translate(target_language)
                    return TextFormatter().format_transcript(translated.fetch()), target_language

                return TextFormatter().format_transcript(transcript.fetch()), original_language

        except Exception as e:
            error_message = str(e).lower()
            if "transcriptsdisabled" in error_message:
                raise ValueError(
                    "This video does not have subtitles/closed captions enabled. "
                    "Available languages: " + ", ".join(available_languages)
                )
            elif "notranscriptfound" in error_message:
                raise ValueError(
                    f"No transcript found for language '{target_language}'. "
                    f"Available languages: {', '.join(available_languages)}"
                )
            else:
                raise ValueError(f"Error fetching transcript: {str(e)}")

    def generate_questions_from_youtube(
        self,
        url: str,
        num: int = 1,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        output_format: Optional[OutputFormatType] = None,
        target_language: str = 'en',
        preserve_original_language: bool = False,
        **kwargs
    ) -> Any:
        try:
            video_id = self._extract_video_id(url)
            transcript, detected_language = self._get_youtube_transcript(video_id, target_language)

            if not transcript:
                raise ValueError("No transcript content retrieved from the video")

            language_context = f"\nContent language: {detected_language}"
            if detected_language != target_language and not preserve_original_language:
                language_context += f"\nGenerate questions in {target_language}"

            video_context = f"\nThis content is from a YouTube video (ID: {video_id}). {language_context}"
            if custom_instructions:
                custom_instructions = video_context + "\n" + custom_instructions
            else:
                custom_instructions = video_context

            return self.generate_questions_from_data(
                source=transcript,
                source_type="text",
                num=num,
                question_type=question_type,
                prompt_template=prompt_template,
                custom_instructions=custom_instructions,
                response_model=response_model,
                output_format=output_format,
                target_language=target_language,
                **kwargs
            )

        except ValueError as ve:
            raise ValueError(f"YouTube processing error: {str(ve)}")
        except Exception as e:
            raise Exception(f"Unexpected error processing YouTube video: {str(e)}")

    def _load_image(self, source: str) -> str:
        try:
            if source.startswith(('http://', 'https://')):
                return source
            elif source.startswith('data:image'):
                return source
            else:
                image = Image.open(source)
                if image.mode not in ('RGB', 'L'):
                    image = image.convert('RGB')
                
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"

        except Exception as e:
            raise ValueError(f"Error loading image: {str(e)}")

    def bulk_generate_questions(
        self,
        topic: Union[str, Path],
        total_questions: Optional[int] = None,
        questions_per_objective: Optional[int] = None, 
        max_workers: Optional[int] = None,
        output_format: Optional[OutputFormatType] = None,
        prompt_template: Optional[str] = None,
        question_model: Type[BaseModel] = BulkMCQ,
        question_list_model: Type[BaseModel] = BulkMCQList,
        min_questions_per_batch: int = 3,
        max_retries: int = 3,
        **kwargs
        ):
        """
        Enhanced bulk question generation with custom response model support.
    
        Args:
            topic: Path to JSON file containing topic structure
            total_questions: Total number of questions to generate
            questions_per_objective: Number of questions to generate per learning objective
            max_workers: Maximum number of concurrent workers
            output_format: Format for output file (pdf, csv, json)
            prompt_template: Custom prompt template (optional)
            question_model: Pydantic model for individual question validation
            question_list_model: Pydantic model for list of questions
            min_questions_per_batch: Minimum questions per batch
            max_retries: Maximum number of retries per batch
            **kwargs: Additional arguments to pass to question generation
        """
        # Initialize variables that might be needed in summary
        base_questions = 0
        remainder = 0
        if isinstance(topic, (Path, str)) and Path(topic).exists():
            with open(Path(topic), 'r') as f:
                    topics_data = json.load(f)
        else:
            raise ValueError("Topic must be a path to a JSON file with the required structure.")
    
        combinations, total_specified, has_question_counts = self._process_topics_data(topics_data)
        total_objectives = len(combinations)
    
        # Determine question distribution based on input parameters
        if questions_per_objective is not None:
            # Override total_questions if questions_per_objective is specified
            total_questions = questions_per_objective * total_objectives
            base_questions = questions_per_objective
            remainder = 0
            question_distribution = {
                f"{combo['topic']}:{combo['subtopic']}:{combo['learning_objective']}": 
                questions_per_objective for combo in combinations
            }
        elif has_question_counts:
            # Use specified counts from JSON
            question_distribution = {
                f"{combo['topic']}:{combo['subtopic']}:{combo['learning_objective']}": 
                combo['num_questions'] for combo in combinations if combo['num_questions'] is not None
            }
            total_questions = total_specified
            base_questions = total_questions // total_objectives
            remainder = total_questions % total_objectives
        else:
            # Use total_questions parameter and distribute evenly
            if total_questions is None:
                total_questions = total_objectives * min_questions_per_batch
    
            base_questions = max(min_questions_per_batch, total_questions // total_objectives)
            remainder = total_questions % total_objectives
    
            question_distribution = {}
            for i, combo in enumerate(combinations):
                extra = 1 if i < remainder else 0
                objective_key = f"{combo['topic']}:{combo['subtopic']}:{combo['learning_objective']}"
                question_distribution[objective_key] = base_questions + extra
                
        all_questions = []
        failed_batches_count = 0
        partial_success_count = 0
    
        # Track failed attempts
        failed_objectives = {
            "timestamp": datetime.now().strftime('%Y%m%d_%H%M%S'),
            "failed_objectives": []
        }
    
        def generate_questions_for_objective(combo):
            """Generate questions for a specific learning objective with failure tracking"""
            nonlocal failed_batches_count, partial_success_count
            retries = 0
            objective_key = f"{combo['topic']}:{combo['subtopic']}:{combo['learning_objective']}"
            target_questions = question_distribution[objective_key]
            accumulated_questions = []
            # print(f"Generating {target_questions} questions for objecjtive: {objective_key}")
    
            failure_record = {
                "topic": combo["topic"],
                "subtopic": combo["subtopic"],
                "learning_objective": combo["learning_objective"],
                "target_questions": target_questions,
                "generated_questions": 0,
                "retry_attempts": [],
            }
    
            while retries < max_retries and len(accumulated_questions) < target_questions:
                try:
                    remaining_questions = target_questions - len(accumulated_questions)
                    batch_result = self._generate_questions_with_retry(
                        combo,
                        remaining_questions,
                        prompt_template=prompt_template,
                        question_model=question_model,
                        question_list_model=question_list_model,
                        is_per_objective=(questions_per_objective is not None),
                        target_questions=target_questions,  # Add this parameter
                        **kwargs
                    )
    
                    attempt_record = {
                        "attempt_number": retries + 1,
                        "timestamp": datetime.now().strftime('%Y%m%d_%H%M%S'),
                        "questions_requested": remaining_questions,
                        "questions_generated": 0,
                        "status": "success",
                        "error": None
                    }
    
                    if batch_result and hasattr(batch_result, 'questions') and batch_result.questions:
                        new_questions = len(batch_result.questions)
                        accumulated_questions.extend(batch_result.questions)
                        attempt_record["questions_generated"] = new_questions
    
                        if len(accumulated_questions) < target_questions:
                            partial_success_count += 1
                            attempt_record["status"] = "partial_success"
                        retries += 1
                    else:
                        attempt_record["status"] = "failed"
                        retries += 1
    
                except Exception as e:
                    attempt_record = {
                        "attempt_number": retries + 1,
                        "timestamp": datetime.now().strftime('%Y%m%d_%H%M%S'),
                        "questions_requested": remaining_questions,
                        "questions_generated": 0,
                        "status": "error",
                        "error": str(e)
                    }
                    retries += 1
    
                failure_record["retry_attempts"].append(attempt_record)
    
            failure_record["generated_questions"] = len(accumulated_questions)
            if len(accumulated_questions) < target_questions:
                failed_objectives["failed_objectives"].append(failure_record)
                if not accumulated_questions:
                    failed_batches_count += 1
                    return None
    
            return question_list_model(questions=accumulated_questions)
    
        # Use ThreadPoolExecutor for parallel processing
        with tqdm(total=len(combinations), desc="Generating questions") as progress_bar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for combo in combinations:
                    future = executor.submit(generate_questions_for_objective, combo)
                    futures.append(future)
    
                for future in concurrent.futures.as_completed(futures):
                    batch_result = future.result()
                    if batch_result and hasattr(batch_result, 'questions') and batch_result.questions:
                        all_questions.extend(batch_result.questions)
                    progress_bar.update(1)
    
        # Handle output formatting for successful questions
        output_file = None
        if output_format and all_questions:
            formatter = OutputFormatter()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
            if output_format == "pdf":
                output_file = formatter.to_pdf(question_list_model(questions=all_questions),
                                            filename=f"questions_{timestamp}.pdf")
            elif output_format == "csv":
                output_file = formatter.to_csv(question_list_model(questions=all_questions),
                                            filename=f"questions_{timestamp}.csv")
            elif output_format == "json":
                output_file = f"questions_{timestamp}.json"
                with open(output_file, 'w') as f:
                    json.dump([q.dict() for q in all_questions], f, indent=4)
    
            print(f"Questions saved to: {output_file}")
    
        # Save failed objectives to JSON if there are any failures
        if failed_objectives["failed_objectives"]:
            failed_file = f"failed_questions_{failed_objectives['timestamp']}.json"
            with open(failed_file, 'w') as f:
                json.dump(failed_objectives, f, indent=4)
            print(f"Failed attempts saved to: {failed_file}")
    
        total_generated = len(all_questions)
        print(f"\n--- Generation Summary ---")
        print(f"Total Learning Objectives: {total_objectives}")
        print(f"Target Total Questions: {total_questions}")
        print(f"Base Questions per Objective: {base_questions} (plus {remainder} objectives with +1)")
        print(f"Total Questions Generated: {total_generated}")
        print(f"Failed Batches: {failed_batches_count}")
        print(f"Partial Success Batches: {partial_success_count}")
        print(f"Average Questions per Successful Batch: {total_generated/(total_objectives-failed_batches_count) if total_generated > 0 else 0:.2f}")
    
        return question_list_model(questions=all_questions), output_file, total_generated, failed_batches_count
    
    def solve_doubt(
        self,
        image_source: str,
        prompt: str = "Explain how to solve this problem",
        custom_instructions: Optional[str] = None,
        detail_level: Literal["low", "medium", "high"] = "medium",
        focus_areas: Optional[List[str]] = None,
        **kwargs
    ) -> SolvedDoubt:
        """
        Analyze an image and provide detailed explanation with solution steps.
        
        Args:
            image_source: Path or URL to the image
            prompt: Custom prompt for analysis
            custom_instructions: Additional instructions for analysis
            detail_level: Level of detail in explanation
            focus_areas: Specific aspects to focus on
            **kwargs: Additional parameters for the model
        
        Returns:
            SolvedDoubt: Object containing explanation, steps, and additional notes
        """
        if not image_source:
            raise ValueError("Image source (path or URL) is required")

        try:
            image_content = self._load_image(image_source)
            
            # Create parser for structured output
            parser = PydanticOutputParser(pydantic_object=SolvedDoubt)
            format_instructions = parser.get_format_instructions()

            # Construct the prompt with all parameters
            base_prompt = f"Analyze the image and {prompt}\n"
            if focus_areas:
                base_prompt += f"\nFocus on these aspects: {', '.join(focus_areas)}"
            base_prompt += f"\nProvide a {detail_level}-detail explanation"
            
            system_message = SystemMessage(
                content="You are a helpful assistant that responds in Markdown. Help with math homework."
            )

            human_message_content = f"""
            {base_prompt}
            
            Provide:
            1. A detailed explanation
            2. Step-by-step solution (if applicable)
            3. Any additional notes or tips
            
            {custom_instructions or ''}
            
            {format_instructions}
            """

            human_message = HumanMessage(content=[
                {"type": "text", "text": human_message_content},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_content,
                        "detail": "high" if detail_level == "high" else "low"
                    }
                }
            ])

            response = self.llm.invoke(
                [system_message, human_message],
                **kwargs
            )

            try:
                return parser.parse(response.content)
            except Exception as e:
                # Fallback if parsing fails
                return SolvedDoubt(
                    explanation=response.content,
                    steps=[],
                    additional_notes="Note: Response format was not structured as requested."
                )

        except Exception as e:
            error_msg = f"Error in solve_doubt: {type(e).__name__}: {str(e)}"
            print(error_msg)
            return SolvedDoubt(
                explanation=error_msg,
                steps=[],
                additional_notes="An error occurred during processing."
            )

   
