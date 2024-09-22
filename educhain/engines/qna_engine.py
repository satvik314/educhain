# educhain/engines/qna_engine.py

from typing import Optional, Type, Any, List, Literal
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

import random

QuestionType = Literal["Multiple Choice", "Short Answer", "True/False", "Fill in the Blank"]

class QnAEngine:
    def __init__(self, llm_config: Optional[LLMConfig] = None):
        if llm_config is None:
            llm_config = LLMConfig()  # Use default OpenAI configuration
        self.llm = self._initialize_llm(llm_config)
        self.embeddings = OpenAIEmbeddings()
        self.pdf_loader = PdfFileLoader()
        self.url_loader = UrlLoader()

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

    def generate_questions(
        self,
        topic: str,
        num: int = 1,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        **kwargs
    ) -> Any:
        parser, model = self._get_parser_and_model(question_type, response_model)
        format_instructions = parser.get_format_instructions()

        if response_model:
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
        **kwargs
    ) -> Any:
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
            return parser.parse(results["result"])
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:", results)
            return model()

    def generate_similar_options(self, question, correct_answer, num_options=3):
        llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)
        prompt = f"Generate {num_options} incorrect but plausible options similar to this correct answer: {correct_answer} for this question: {question}. Provide only the options, separated by semicolons. The options should not precede or end with any symbols, it should be similar to the correct answer."
        response = llm.predict(prompt)
        return response.split(';')

    def generate_mcq_math(self, topic, num=1, llm=None, response_model=None,
                         prompt_template=None, custom_instructions=None, **kwargs):
        if response_model is None:
            parser = PydanticOutputParser(pydantic_object=MCQListMath)
            format_instructions = parser.get_format_instructions()
        else:
            parser = PydanticOutputParser(pydantic_object=response_model)
            format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            You are an Academic AI assistant tasked with generating multiple-choice questions on various topics specialised in Maths Subject.
            Generate {num} multiple-choice question (MCQ) based on the given topic and level.
            provide the question, four answer options, and the correct answer.

            Topic: {topic}
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\nThe response should be in JSON format. \n {format_instructions}"

        MCQ_prompt = PromptTemplate(
            input_variables=["num", "topic"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        if llm:
            llm = llm
        else:
            llm = self.llm  # Use the initialized LLM from the class

        MCQ_chain = MCQ_prompt | llm

        results = MCQ_chain.invoke(
            {"num": num, "topic": topic, **kwargs},
        )
        results = results.content
        structured_output = parser.parse(results)

        llm_math = LLMMathChain.from_llm(llm=llm, verbose=False)

        for question in structured_output.questions:
            if question.requires_math:
                try:
                    with get_openai_callback() as cb:
                        result = llm_math.invoke({"question": question.question})
                        result = result['result'].strip().split(":")[-1]
                        result = float(result)
                        result = f"{result: .2f}"

                    question.explanation += f"\n\nMath solution: {result}"

                    correct_option = Option(text=str(result.lstrip()), correct='true')
                    incorrect_options = [Option(text=opt.strip(), correct='false')
                                         for opt in self.generate_similar_options(question.question, result)]

                    while len(incorrect_options) < 3:
                        incorrect_options.append(Option(text="N/A", correct='false'))

                    question.options = [correct_option] + incorrect_options[:3]
                    random.shuffle(question.options)
                except Exception as e:
                    print(f"LLMMathChain failed to answer: {str(e)}")
        return structured_output