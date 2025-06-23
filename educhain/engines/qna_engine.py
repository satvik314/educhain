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
    FillInBlankQuestionList, MCQListMath, Option, SolvedDoubt, SpeechInstructions,
    VisualMCQList, VisualMCQ, BulkMCQ, BulkMCQList, ShortAnswerQuestion, TrueFalseQuestion, FillInBlankQuestion,
    BulkShortAnswerQuestion, BulkShortAnswerQuestionList,
    BulkTrueFalseQuestion, BulkTrueFalseQuestionList,
    BulkFillInBlankQuestion, BulkFillInBlankQuestionList
)
from educhain.utils.loaders import PdfFileLoader, UrlLoader
from educhain.utils.output_formatter import OutputFormatter
import base64
import os
from PIL import Image
import io
import csv
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
DEFAULT_PROMPT_TEMPLATE ="""
Generate multiple-choice questions for the following topic and learning objective:
Topic: {topic}
Subtopic: {subtopic}
Learning Objective: {learning_objective}

Each question should:
1. Be clear and concise
2. Test understanding of the specific learning objective
3. Include a detailed explanation of the answer
4. Be appropriate for 5th grade level
5. Be of medium difficulty

Generate {num} questions in the following JSON format:
{{
    "questions": [
        {{
            "question": "The question text",
            "options": [
                {{"text": "Option A", "correct": "true"}},
                {{"text": "Option B", "correct": "false"}},
                {{"text": "Option C", "correct": "false"}},
                {{"text": "Option D", "correct": "false"}}
            ],
            "explanation": "Detailed explanation of why the answer is correct",
            "difficulty": "medium",
            "metadata": {{
                "topic": "{topic}",
                "subtopic": "{subtopic}",
                "learning_objective": "{learning_objective}"
            }}
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
                base_template += "\n4. A list of relevant keywords and the answer should be in text form not options"
            elif question_type == "True/False":
                base_template += "\n4. The correct answer as a boolean (true/false) and the genrated question follow True/False pattern"
            elif question_type == "Fill in the Blank":
                base_template += "\n4. The word or phrase to be filled in the blank and the question should follow Fill in the Blank Style only"

            return base_template


    def _create_vector_store(self, content: str) -> Chroma:
        if self.embeddings is None:
            self.embeddings = OpenAIEmbeddings()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
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
        learning_objective: Optional[str] = None,
        difficulty_level: Optional[str] = None,
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

        # Add learning objective and difficulty level if provided
        if learning_objective or difficulty_level:
            template += """
            Learning Objective: {learning_objective}
            Difficulty Level: {difficulty_level}

            Ensure that the questions are relevant to the learning objective and match the specified difficulty level.
            """

        template += """
        The response should be in JSON format.
        {format_instructions}
        """

        if custom_instructions:
            template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        question_prompt = PromptTemplate(
            input_variables=["num", "topic", "learning_objective", "difficulty_level"],
            template=template,
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
            **kwargs: Additional parameters to pass to the model
        
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

    def _read_questions_from_csv(self, csv_filepath):
        """Read existing questions from a CSV file and return a set of question texts"""
        existing_questions = set()
        
        try:
            if not os.path.exists(csv_filepath) or os.path.getsize(csv_filepath) == 0:
                return existing_questions
                
            with open(csv_filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Try different common field names for question text
                    question_fields = ['question', 'question_text', 'stem', 'prompt']
                    for field in question_fields:
                        if field in row and row[field]:
                            existing_questions.add(row[field].strip())
                            break
                            
        except Exception as e:
            print(f"Warning: Error reading existing questions from CSV: {e}")
            
        return existing_questions

    def _write_questions_to_csv(self, questions, csv_filepath, question_model, append=False, check_duplicates=False):
        """
        Write questions to CSV file, either creating a new file or appending to an existing one.
        Checks for duplicates if check_duplicates is True.
        
        Returns: List of questions that were actually written (non-duplicates)
        """
        mode = 'a' if append else 'w'
        
        # If checking duplicates, read existing questions
        existing_questions = set()
        if check_duplicates and append:
            existing_questions = self._read_questions_from_csv(csv_filepath)

        # Dynamically determine fieldnames from the model
        model_fields = list(question_model.__annotations__.keys())

        
        written_questions = []
        
        with open(csv_filepath, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=model_fields)
            
            # Write header only if creating a new file
            if not append:
                writer.writeheader()
            
            # Write each question to the CSV file
            for question in questions:
                q_dict = question.dict() if hasattr(question, 'dict') else question
                
                # Check for duplicates
                duplicate = False
                if existing_questions:
                    # Try different common field names for question text
                    question_fields = ['question', 'question_text', 'stem', 'prompt']
                    for field in question_fields:
                        if field in q_dict and q_dict[field] and q_dict[field].strip() in existing_questions:
                            duplicate = True
                            break
                    
                if duplicate:
                    continue
                    
                # Add metadata if missing
                if 'metadata' not in q_dict and hasattr(question_model, '__fields__') and 'metadata' in question_model.__fields__:
                    q_dict['metadata'] = {
                        "topic": combo["topic"],
                        "subtopic": combo["subtopic"],
                        "learning_objective": combo["learning_objective"]
                    }

                validated_question = self._validate_individual_question(q_dict, question_model=question_model)
                if validated_question:
                    batch_validated_questions.append(validated_question)
                        
                    # Add to existing questions to prevent duplicates in future batches
                    if csv_output_file:
                        for field in ['question', 'question_text', 'stem', 'prompt']:
                            if field in q_dict and q_dict[field]:
                                existing_questions.add(q_dict[field].strip())
                                break

                # Process complex fields to convert to JSON strings
                row_data = {}
                
                # First, add all simple fields directly
                for field_name in model_fields:
                    value = q_dict.get(field_name)
                    
                    # Special handling for keywords in short answer questions
                    if field_name == 'keywords' and isinstance(value, list):
                        # Format keywords as comma-separated string instead of JSON
                        row_data[field_name] = ', '.join(value)
                    # Special handling for boolean (true/false) values
                    elif field_name == 'answer' and isinstance(value, bool):
                        # Convert boolean to 'True' or 'False' string
                        row_data[field_name] = str(value)
                    # Skip context field for Fill in the Blank questions
                    elif field_name == 'context':
                        continue
                    # Simple values go in directly
                    elif not isinstance(value, (dict, list)) and not hasattr(value, 'dict'):
                        row_data[field_name] = value
                    # Handle complex objects
                    else:
                        if hasattr(value, 'dict'):
                            value = value.dict()
                        row_data[field_name] = json.dumps(value)
                
                # Write to CSV and track which questions were written        
                writer.writerow(row_data)
                written_questions.append(question)
                
                # Add to existing questions set to prevent duplicates within the current batch
                if check_duplicates:
                    for field in question_fields:
                        if field in q_dict and q_dict[field]:
                            existing_questions.add(q_dict[field].strip())
                            break
        
        return written_questions

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
                                   csv_output_file=None,
                                   question_type="Multiple Choice",
                                   **kwargs):
        """
        Generate questions with improved retry mechanism and chunking.
        Includes duplicate checking if csv_output_file is provided.
        Now supports different question types.
        """
        MAX_QUESTIONS_PER_BATCH = 3
        MAX_DUPLICATE_RETRIES = 3  # Maximum retries for a batch with duplicates
        validated_questions = []
        remaining_questions = num_questions if not target_questions else target_questions
        total_attempts = 0
        max_attempts = max(5, (remaining_questions // MAX_QUESTIONS_PER_BATCH) * 2)
        
        # Get existing questions if csv_output_file is provided
        existing_questions = set()
        if csv_output_file:
            existing_questions = self._read_questions_from_csv(csv_output_file)

        while remaining_questions > 0 and len(validated_questions) < (target_questions or num_questions) and total_attempts < max_attempts:
            try:
                # Calculate batch size based on remaining questions
                current_batch_size = min(MAX_QUESTIONS_PER_BATCH, remaining_questions)
                
                # Generate the batch with specified question type
                batch_questions = self.generate_questions(
                    topic=combo["topic"],
                    num=current_batch_size,
                    question_type=question_type,  # Use the specified question type
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

                # Validate questions and check for duplicates
                batch_validated_questions = []
                duplicate_count = 0
                target_reached = False
                
                for question in questions_to_validate:
                    # Stop if we've already collected enough questions
                    if len(validated_questions) >= (target_questions or num_questions):
                        target_reached = True
                        break

                    question_dict = question.dict() if hasattr(question, 'dict') else question
                    
                    # Check for duplicates
                    duplicate = False
                    if existing_questions:
                        # Try different common field names for question text
                        question_fields = ['question', 'question_text', 'stem', 'prompt']
                        for field in question_fields:
                            if field in question_dict and question_dict[field] and question_dict[field].strip() in existing_questions:
                                duplicate = True
                                duplicate_count += 1
                                print(f"Duplicate question detected: '{question_dict[field][:50]}...'")
                                break
                    
                    if duplicate:
                        continue
                    
                    # Add metadata if missing
                    if 'metadata' not in question_dict and hasattr(question_model, '__fields__') and 'metadata' in question_model.__fields__:
                        question_dict['metadata'] = {
                            "topic": combo["topic"],
                            "subtopic": combo["subtopic"],
                            "learning_objective": combo["learning_objective"]
                        }

                    validated_question = self._validate_individual_question(question_dict, question_model=question_model)
                    if validated_question:
                        batch_validated_questions.append(validated_question)
                        
                        # Add to existing questions to prevent duplicates in future batches
                        if csv_output_file:
                            for field in ['question', 'question_text', 'stem', 'prompt']:
                                if field in question_dict and question_dict[field]:
                                    existing_questions.add(question_dict[field].strip())
                                    break

                # If we found duplicates but no valid questions in this batch, retry with a clear instruction
                if duplicate_count > 0 and not batch_validated_questions and total_attempts < MAX_DUPLICATE_RETRIES:
                    print(f"All questions in batch were duplicates. Regenerating with explicit uniqueness instruction...")
                    custom_instructions = kwargs.get('custom_instructions', '')
                    if custom_instructions:
                        custom_instructions = f"{custom_instructions}\n\nIMPORTANT: Generate completely new and unique questions that are different from previous ones."
                    else:
                        custom_instructions = "IMPORTANT: Generate completely new and unique questions that are different from previous ones."
                    kwargs['custom_instructions'] = custom_instructions
                    total_attempts += 1
                    continue
                
                # Add valid questions to our collection, but only as many as we need
                space_remaining = (target_questions or num_questions) - len(validated_questions)
                questions_to_add = min(len(batch_validated_questions), space_remaining)
                
                validated_questions.extend(batch_validated_questions[:questions_to_add])
                remaining_questions = (target_questions or num_questions) - len(validated_questions)
                total_attempts += 1
                
                # If we've reached our target, break out of the loop
                if target_reached or remaining_questions == 0:
                    break

            except Exception as e:
                print(f"Error in generation attempt {total_attempts + 1}: {str(e)}")
                total_attempts += 1
                if not validated_questions:
                    continue

        return question_list_model(questions=validated_questions)

    def generate_questions_for_objective(self, combo, question_distribution, 
                                        prompt_template, question_model, question_list_model, 
                                        questions_per_objective, csv_output_file, max_retries, 
                                        question_type="Multiple Choice", **kwargs):
        """Generate questions for a specific learning objective with failure tracking, CSV saving, and duplicate checking"""
        retries = 0
        objective_key = f"{combo['topic']}:{combo['subtopic']}:{combo['learning_objective']}"
        target_questions = question_distribution[objective_key]
        accumulated_questions = []
        duplicates_count = 0

        failure_record = {
            "topic": combo["topic"],
            "subtopic": combo["subtopic"],
            "learning_objective": combo["learning_objective"],
            "question_type": question_type,  # Add question type to the failure record
            "target_questions": target_questions,
            "generated_questions": 0,
            "duplicate_questions": 0,
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
                    target_questions=remaining_questions,
                    csv_output_file=csv_output_file,
                    question_type=question_type,  # Pass the question type
                    **kwargs
                )
                
                attempt_record = {
                    "attempt_number": retries + 1,
                    "timestamp": datetime.now().strftime('%Y%m%d_%H%M%S'),
                    "questions_requested": remaining_questions,
                    "questions_generated": 0,
                    "questions_duplicated": 0,
                    "status": "success",
                    "error": None
                }

                if batch_result and hasattr(batch_result, 'questions') and batch_result.questions:
                    # Ensure we only process exactly the number of questions we need
                    questions_to_process = batch_result.questions[:remaining_questions]
                    
                    # Write to CSV and get only the non-duplicate questions that were written
                    original_count = len(questions_to_process)
                    written_questions = self._write_questions_to_csv(
                        questions_to_process, 
                        csv_output_file, 
                        question_model, 
                        append=True,
                        check_duplicates=True
                    )
                    
                    # Count duplicates
                    num_duplicates = original_count - len(written_questions)
                    duplicates_count += num_duplicates
                    attempt_record["questions_duplicated"] = num_duplicates
                    
                    # Add only non-duplicate questions
                    new_questions = len(written_questions)
                    
                    # Check if we'd exceed our target and truncate if necessary
                    space_left = target_questions - len(accumulated_questions)
                    if new_questions > space_left:
                        written_questions = written_questions[:space_left]
                        new_questions = len(written_questions)
                    
                    accumulated_questions.extend(written_questions)
                    attempt_record["questions_generated"] = new_questions

                    if len(accumulated_questions) < target_questions:
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
                    "questions_duplicated": 0,
                    "status": "error",
                    "error": str(e)
                }
                retries += 1

            failure_record["retry_attempts"].append(attempt_record)

        failure_record["generated_questions"] = len(accumulated_questions)
        failure_record["duplicate_questions"] = duplicates_count
        return accumulated_questions, failure_record

    def bulk_generate_questions(
        self,
        topic: Union[str, Path],
        total_questions: Optional[int] = None,
        questions_per_objective: Optional[int] = None, 
        max_workers: Optional[int] = None,
        output_format: Optional[OutputFormatType] = None,
        prompt_template: Optional[str] = None,
        question_type: QuestionType = "Multiple Choice",
        question_model: Type[BaseModel] = None,
        question_list_model: Type[BaseModel] = None,
        min_questions_per_batch: int = 3,
        max_retries: int = 3,
        **kwargs
    ):
        """
        Enhanced bulk question generation with continuous CSV saving and duplicate checking.
        Ensures exactly the target number of questions are generated per objective.
        Supports different question types.

        Args:
            topic: Path to JSON file containing topic structure
            total_questions: Total number of questions to generate
            questions_per_objective: Number of questions to generate per learning objective
            max_workers: Maximum number of concurrent workers
            output_format: Format for output file (pdf, csv, json)
            prompt_template: Custom prompt template (optional)
            question_type: Type of question to generate (Multiple Choice, Short Answer, True/False, Fill in the Blank)
            question_model: Pydantic model for individual question validation (default: based on question_type)
            question_list_model: Pydantic model for list of questions (default: based on question_type)
            min_questions_per_batch: Minimum questions per batch
            max_retries: Maximum number of retries per batch
            **kwargs: Additional arguments to pass to question generation
        """
        # Set default models based on question_type if not specified
        if question_model is None or question_list_model is None:
            if question_type == "Multiple Choice":
                question_model = question_model or BulkMCQ
                question_list_model = question_list_model or BulkMCQList
            elif question_type == "Short Answer":
                question_model = question_model or BulkShortAnswerQuestion 
                question_list_model = question_list_model or BulkShortAnswerQuestionList
            elif question_type == "True/False":
                question_model = question_model or BulkTrueFalseQuestion
                question_list_model = question_list_model or BulkTrueFalseQuestionList
            elif question_type == "Fill in the Blank":
                question_model = question_model or BulkFillInBlankQuestion
                question_list_model = question_list_model or BulkFillInBlankQuestionList
            else:
                # Default to Multiple Choice if question_type is unsupported
                question_model = question_model or BulkMCQ
                question_list_model = question_list_model or BulkMCQList
                
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

        # Initialize CSV file for continuous saving
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_output_file = f"questions_{timestamp}.csv"
        # Create empty CSV file with headers
        self._write_questions_to_csv([], csv_output_file, question_model)
        print(f"Created CSV file for continuous saving: {csv_output_file}")

        all_questions = []
        failed_batches_count = 0
        partial_success_count = 0
        duplicates_count = 0

        # Track failed attempts
        failed_objectives = {
            "timestamp": timestamp,
            "failed_objectives": []
        }

        # Use ThreadPoolExecutor for parallel processing
        with tqdm(total=len(combinations), desc=f"Generating {question_type} questions") as progress_bar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {}
                for combo in combinations:
                    future = executor.submit(
                        self.generate_questions_for_objective,
                        combo=combo,
                        question_distribution=question_distribution,
                        prompt_template=prompt_template,
                        question_model=question_model,
                        question_list_model=question_list_model,
                        questions_per_objective=questions_per_objective,
                        csv_output_file=csv_output_file,
                        max_retries=max_retries,
                        question_type=question_type,  # Pass question_type to generation function
                        **kwargs
                    )
                    futures[future] = combo

                for future in concurrent.futures.as_completed(futures):
                    combo = futures[future]
                    try:
                        accumulated_questions, failure_record = future.result()
                        
                        # Update statistics
                        if failure_record["duplicate_questions"] > 0:
                            duplicates_count += failure_record["duplicate_questions"]
                            
                        # Handle failure records
                        objective_key = f"{combo['topic']}:{combo['subtopic']}:{combo['learning_objective']}"
                        target = question_distribution[objective_key]
                        
                        if len(accumulated_questions) < target:
                            if len(accumulated_questions) == 0:
                                failed_batches_count += 1
                            else:
                                partial_success_count += 1
                            failed_objectives["failed_objectives"].append(failure_record)
                        
                        # Add questions to our master list
                        if accumulated_questions:
                            all_questions.extend(accumulated_questions)
                            
                    except Exception as e:
                        print(f"Error processing objective {combo['topic']} - {combo['subtopic']} - {combo['learning_objective']}: {str(e)}")
                        failed_batches_count += 1
                        
                    progress_bar.update(1)

        # Handle additional output formatting for successful questions
        output_file = csv_output_file  # Default output file is the CSV we've been writing to
        
        # Generate additional formats if requested
        if output_format and output_format != "csv" and all_questions:
            if output_format == "pdf":
                pdf_output_file = f"questions_{timestamp}.pdf"
                
                try:
                    from reportlab.lib.pagesizes import letter
                    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                    from reportlab.lib import colors
                    
                    # Create PDF document
                    doc = SimpleDocTemplate(pdf_output_file, pagesize=letter)
                    styles = getSampleStyleSheet()
                    
                    # Create custom styles
                    title_style = styles["Heading1"]
                    question_style = ParagraphStyle(
                        'QuestionStyle',
                        parent=styles['Normal'],
                        fontName='Helvetica-Bold',
                        fontSize=12,
                        leading=14,
                        spaceAfter=6
                    )
                    explanation_style = ParagraphStyle(
                        'ExplanationStyle',
                        parent=styles['Normal'],
                        fontName='Helvetica-Oblique',
                        fontSize=10,
                        leading=12,
                        leftIndent=20,
                        spaceAfter=12
                    )
                    normal_style = styles["Normal"]
                    
                    # Build PDF content
                    elements = []
                    
                    # Add title
                    elements.append(Paragraph(f"Generated Questions - {timestamp}", title_style))
                    elements.append(Spacer(1, 12))
                    
                    # Add questions
                    for i, question in enumerate(all_questions, 1):
                        # Get question data as dictionary
                        q_dict = question.dict() if hasattr(question, 'dict') else question
                        
                        # Add question number and find main question text
                        # Try common field names for question text
                        question_fields = ['question', 'question_text', 'stem', 'prompt']
                        question_text = None
                        for field in question_fields:
                            if field in q_dict:
                                question_text = q_dict.get(field)
                                break
                                
                        # Default if no standard field found
                        if question_text is None:
                            # Try to find the most likely question field (the longest text field)
                            text_fields = {k: v for k, v in q_dict.items() 
                                        if isinstance(v, str) and len(v) > 10 and k not in ['explanation']}
                            if text_fields:
                                question_text = text_fields[max(text_fields, key=lambda k: len(text_fields[k]))]
                            else:
                                question_text = str(q_dict)
                        
                        # Add the question text
                        elements.append(Paragraph(f"Question {i}: {question_text}", question_style))
                        elements.append(Spacer(1, 6))
                        
                        # For True/False questions, specifically show the answer
                        if question_type == "True/False" and 'answer' in q_dict:
                            answer_value = q_dict['answer']
                            if isinstance(answer_value, bool) or answer_value in ('True', 'False', 'true', 'false'):
                                # Format the answer for display
                                formatted_answer = str(answer_value).capitalize()
                                elements.append(Paragraph(f"Answer: {formatted_answer}", normal_style))
                                elements.append(Spacer(1, 6))
                        # For Fill in the Blank, always show the answer
                        elif question_type == "Fill in the Blank" and 'answer' in q_dict:
                            elements.append(Paragraph(f"Answer: {q_dict['answer']}", normal_style))
                            elements.append(Spacer(1, 6))
                        # For Short Answer questions, show the answer
                        elif question_type == "Short Answer" and 'answer' in q_dict:
                            elements.append(Paragraph(f"Answer: {q_dict['answer']}", normal_style))
                            elements.append(Spacer(1, 6))
                            
                            # Also show keywords if they exist
                            if 'keywords' in q_dict and q_dict['keywords']:
                                # Handle keywords that might be stored as JSON string
                                keywords = q_dict['keywords']
                                if isinstance(keywords, str):
                                    # Try to parse if it's a JSON string
                                    try:
                                        keywords = json.loads(keywords)
                                    except (json.JSONDecodeError, TypeError):
                                        # If not valid JSON, it's likely already a comma-separated string
                                        # or keep as is if parsing fails
                                        pass
                                        
                                # Format keywords for display
                                if isinstance(keywords, list):
                                    keywords_str = ", ".join(keywords)
                                elif isinstance(keywords, str):
                                    keywords_str = keywords
                                else:
                                    keywords_str = str(keywords)
                                    
                                elements.append(Paragraph(f"Keywords: {keywords_str}", normal_style))
                                elements.append(Spacer(1, 6))
                        
                        # Handle additional fields that aren't standard
                        for key, value in q_dict.items():
                            # Skip already shown question text, context, and common fields
                            if (key in question_fields or 
                                key in ['options', 'explanation', 'difficulty', 'difficulty_level', 'metadata', 'context', 'answer']):
                                continue
                            
                            # Only show string values with reasonable length
                            if isinstance(value, str) and 5 < len(value) < 1000:
                                label = key.replace('_', ' ').title()
                                elements.append(Paragraph(f"{label}: {value}", normal_style))
                                elements.append(Spacer(1, 4))
                        
                        # Add options in a table format
                        if 'options' in q_dict and q_dict.get('options'):
                            options_data = []
                            options = q_dict.get('options', [])
                            correct_answer = None
                            
                            for j, option in enumerate(options):
                                option_letter = chr(65 + j)  # A, B, C, D
                                
                                # Handle different option formats
                                if isinstance(option, dict):
                                    option_text = option.get('text', None)
                                    if option_text is None:  # If no 'text' field, use first string field found
                                        for field, value in option.items():
                                            if isinstance(value, str) and len(value) > 1:
                                                option_text = value
                                                break
                                    if option_text is None:  # If still no text found, use the string representation
                                        option_text = str(option)
                                        
                                    # Try all possible correct field names
                                    correct_fields = ['correct', 'is_correct', 'isCorrect', 'is_answer']
                                    is_correct = False
                                    for field in correct_fields:
                                        if field in option:
                                            value = option.get(field)
                                            if isinstance(value, bool):
                                                is_correct = value
                                            elif isinstance(value, str):
                                                is_correct = value.lower() in ['true', 't', 'yes', 'y', '1']
                                            break
                                elif hasattr(option, 'dict'):  # Pydantic model
                                    option_dict = option.dict()
                                    option_text = option_dict.get('text', str(option))
                                    is_correct = option_dict.get('correct', False)
                                else:
                                    option_text = str(option)
                                    is_correct = False
                                    
                                # Format the option
                                option_row = [f"{option_letter}.", option_text]
                                options_data.append(option_row)
                                
                                # Track correct answer
                                if is_correct:
                                    correct_answer = f"Correct Answer: {option_letter}"
                            
                            # Create options table only if we have options
                            if options_data:
                                options_table = Table(options_data, colWidths=[30, 450])
                                options_table.setStyle(TableStyle([
                                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                                    ('LEFTPADDING', (0, 0), (0, -1), 0),
                                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                                ]))
                                elements.append(options_table)
                                elements.append(Spacer(1, 6))
                                
                                # Add correct answer if found
                                if correct_answer:
                                    elements.append(Paragraph(correct_answer, styles["Heading4"]))
                                    elements.append(Spacer(1, 6))
                        
                        # Add explanation if it exists
                        explanation = q_dict.get('explanation', '')
                        if explanation:
                            elements.append(Paragraph(f"Explanation: {explanation}", explanation_style))
                            elements.append(Spacer(1, 6))
                        
                        # Add difficulty if it exists - try multiple common field names
                        difficulty_fields = ['difficulty', 'difficulty_level']
                        for field in difficulty_fields:
                            if field in q_dict and q_dict[field]:
                                elements.append(Paragraph(f"Difficulty: {q_dict[field]}", normal_style))
                                elements.append(Spacer(1, 4))
                                break
                        
                        # Handle additional fields that aren't standard
                        for key, value in q_dict.items():
                            if (key.endswith('_rating') or key.startswith('difficulty_') or 
                                key.endswith('_time') or key.endswith('_score')) and key not in difficulty_fields:
                                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '').isdigit()):
                                    label = key.replace('_', ' ').title()
                                    elements.append(Paragraph(f"{label}: {value}", normal_style))
                                    elements.append(Spacer(1, 4))
                        
                        # Add metadata if it exists
                        metadata = q_dict.get('metadata', {})
                        if metadata:
                            if isinstance(metadata, dict):
                                metadata_text = ", ".join([f"{k}: {v}" for k, v in metadata.items()])
                                elements.append(Paragraph(f"Metadata: {metadata_text}", normal_style))
                            elif isinstance(metadata, str):
                                elements.append(Paragraph(f"Metadata: {metadata}", normal_style))
                        
                        # Add separator between questions
                        elements.append(Spacer(1, 20))
                    
                    # Build the PDF
                    doc.build(elements)
                    print(f"Questions saved to PDF: {pdf_output_file}")
                    output_file = pdf_output_file
                
                except Exception as e:
                    print(f"Error generating PDF: {str(e)}")
                    # PDF generation failed but we already have the CSV

            elif output_format == "json":
                json_output_file = f"questions_{timestamp}.json"
                with open(json_output_file, 'w') as f:
                    json.dump([q.dict() if hasattr(q, 'dict') else q for q in all_questions], f, indent=4)
                print(f"Questions saved to JSON: {json_output_file}")
                output_file = json_output_file

        # Save failed objectives to JSON if there are any failures
        if failed_objectives["failed_objectives"]:
            failed_file = f"failed_questions_{failed_objectives['timestamp']}.json"
            with open(failed_file, 'w') as f:
                json.dump(failed_objectives, f, indent=4)
            print(f"Failed attempts saved to: {failed_file}")

        # Modified summary section to include duplicate stats
        total_generated = len(all_questions)
        print(f"\n--- Generation Summary ---")
        print(f"Total Learning Objectives: {total_objectives}")
        print(f"Target Total Questions: {total_questions}")
        print(f"Base Questions per Objective: {base_questions} (plus {remainder} objectives with +1)")
        print(f"Total Questions Generated: {total_generated}")
        print(f"Duplicate Questions Detected: {duplicates_count}")
        print(f"Failed Batches: {failed_batches_count}")
        print(f"Partial Success Batches: {partial_success_count}")
        print(f"Average Questions per Successful Batch: {total_generated/(total_objectives-failed_batches_count) if total_generated > 0 else 0:.2f}")
        print(f"Questions continuously saved to: {csv_output_file}")

        return question_list_model(questions=all_questions), output_file, total_generated, failed_batches_count
