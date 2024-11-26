# educhain/engines/qna_engine.py

from typing import Optional, Type, Any, List, Literal, Union, Tuple
from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, RetrievalQA, LLMMathChain
from langchain.output_parsers import PydanticOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.callbacks.manager import get_openai_callback

from educhain.core.config import LLMConfig
from educhain.models.qna_models import (
    MCQList, ShortAnswerQuestionList, TrueFalseQuestionList, 
    FillInBlankQuestionList, MCQListMath, Option
)
from educhain.utils.loaders import PdfFileLoader, UrlLoader
from educhain.utils.output_formatter import OutputFormatter

# Update the QuestionType definition

import random

QuestionType = Literal["Multiple Choice", "Short Answer", "True/False", "Fill in the Blank"]
OutputFormatType = Literal["pdf", "csv"]

class QnAEngine:
    def __init__(self, llm_config: Optional[LLMConfig] = None):
        if llm_config is None:
            llm_config = LLMConfig()  # Use default OpenAI configuration
        self.llm = self._initialize_llm(llm_config)
        self.pdf_loader = PdfFileLoader()
        self.url_loader = UrlLoader()
        self.embeddings = None  # Initialize as None

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
        else:
            raise ValueError(f"Unsupported question type: {question_type}")

    def _get_prompt_template(self, question_type: QuestionType, custom_template: Optional[str] = None):
        if custom_template:
            return custom_template

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
        # Ensure embeddings are initialized
        if self.embeddings is None:
            self.embeddings = OpenAIEmbeddings()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(content)

        # Create the vector store
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
        """Handle output format conversion if specified"""
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

        if response_model:
            if prompt_template:
                template = prompt_template
            else:
                template = """
                Generate {num} questions based on the given topic.
                Topic: {topic}

                Ensure that each question follows the structure specified in the format instructions.
                """
        else:
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
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results)
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
        # Initialize embeddings only when this method is called
        if self.embeddings is None:
            self.embeddings = OpenAIEmbeddings()

        content = self._load_data(source, source_type)

        vector_store = self._create_vector_store(content)
        qa_chain = self._setup_retrieval_qa(vector_store)

        parser, model = self._get_parser_and_model(question_type, response_model)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = self._get_prompt_template(question_type)

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
            topic=content[:1000],  # Use a subset of content to fit in context
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
            print(f"Error parsing output: {e}")
            print("Raw output:", results)
            return model()

    def generate_similar_options(self, question, correct_answer, num_options=3):
        llm = self.llm
        prompt = f"Generate {num_options} incorrect but plausible options similar to this correct answer: {correct_answer} for this question: {question}. Provide only the options, separated by semicolons. The options should not precede or end with any symbols, it should be similar to the correct answer."
        response = llm.predict(prompt)
        return response.split(';')

    def _process_math_result(self, math_result: Any) -> str:
        """Helper method to process and extract numerical answer from LLMMathChain result"""
        if isinstance(math_result, dict):
            if 'answer' in math_result:
                return math_result['answer'].split('Answer: ')[-1].strip()
            elif 'result' in math_result:
                return math_result['result'].strip()
        
        # Handle string response
        result_str = str(math_result)
        if 'Answer:' in result_str:
            return result_str.split('Answer:')[-1].strip()
        
        # Remove any question repetition and extract the numerical result
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

        if prompt_template is None:
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
            print(results)
            return MCQListMath()

        llm_math = LLMMathChain.from_llm(llm=self.llm, verbose=True)

        for question in structured_output.questions:
            if question.requires_math:
                try:
                    # Extract numerical expression from the question
                    math_result = llm_math.invoke({"question": question.question})
                    
                    try:
                        # Process the result using the helper method
                        solution = self._process_math_result(math_result)
                        
                        # Convert to float and format
                        numerical_solution = float(solution)
                        formatted_solution = f"{numerical_solution:.2f}"
                        
                        question.explanation += f"\n\nMath solution: {formatted_solution}"
                        
                        # Generate options with the correct string format
                        correct_option = Option(text=formatted_solution, correct='true')
                        
                        # Generate incorrect options
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
                        
                        # Combine and shuffle options
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
