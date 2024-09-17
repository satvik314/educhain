from typing import List, Optional, Any, Literal
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from .models import MCQList, QuestionList, MultipleChoiceQuestion, ShortAnswerQuestionList, TrueFalseQuestionList, FillInBlankQuestionList ,PdfFileLoader,UrlLoader
from .config import EduchainConfig, LLMConfig
from langchain_community.document_loaders import YoutubeLoader
import time
import os
from supabase import create_client

class QnAEngine:
    def __init__(self, config: EduchainConfig):
        self.config = config
        self.llm = self._initialize_llm()


    def _initialize_llm(self):
        llm_config = self.config.llm_config
        if llm_config.custom_model:
            return llm_config.custom_model
        else:
            # Fallback to OpenAI or other default implementation
            return ChatOpenAI(
                model=llm_config.model_name,
                api_key=llm_config.api_key,
                max_tokens=llm_config.max_tokens,
                temperature=llm_config.temperature,
                base_url=llm_config.base_url,
                default_headers=llm_config.default_headers
            )

    def generate_mcq(self, topic: str, num: int = 1, prompt_template: Optional[str] = None, custom_instructions: Optional[str] = None, **kwargs) -> MCQList:
        parser = PydanticOutputParser(pydantic_object=MCQList)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
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

        MCQ_chain = MCQ_prompt | self.llm

        results = MCQ_chain.invoke(
            {"num": num, "topic": topic, **kwargs},
        )

        results = results.content
        structured_output = parser.parse(results)

        return structured_output


    QuestionType = Literal["Multiple Choice", "Short Answer", "True/False", "Fill in the Blank"]


    def generate_questions(self, topic: str, num: int = 1, type: QuestionType = "Multiple Choice", prompt_template: Optional[str] = None, custom_instructions: Optional[str] = None, **kwargs) -> QuestionList:
        if type == "Multiple Choice":
            parser = PydanticOutputParser(pydantic_object=MCQList)
        elif type == "Short Answer":
            parser = PydanticOutputParser(pydantic_object=ShortAnswerQuestionList)
        elif type == "True/False":
            parser = PydanticOutputParser(pydantic_object=TrueFalseQuestionList)
        elif type == "Fill in the Blank":
            parser = PydanticOutputParser(pydantic_object=FillInBlankQuestionList)
        else:
            raise ValueError(f"Unsupported question type: {type}")

        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = f"""
            Generate {{num}} {type} question(s) based on the given topic.
            Topic: {{topic}}

            For each question, provide:
            1. The question
            2. The correct answer
            3. An explanation (optional)
            """

            if type == "Multiple Choice":
                prompt_template += "\n4. A list of options (including the correct answer)"
            elif type == "Short Answer":
                prompt_template += "\n4. A list of relevant keywords"
            elif type == "True/False":
                prompt_template += "\n4. The correct answer as a boolean (true/false)"
            elif type == "Fill in the Blank":
                prompt_template += "\n4. The word or phrase to be filled in the blank"

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\n\nThe response should be in JSON format.\n{format_instructions}"

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
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results)
            return QuestionList(questions=[])

##feature to add RAG! use_rag = True

    def generate_mcqs_from_data(self, source: str, source_type: str, num: int = 1, learning_objective: str = "", difficulty_level: str = "", prompt_template: Optional[str] = None, **kwargs) -> MCQList:
        # Load data based on source type
        if source_type == 'pdf':
            loader = PdfFileLoader()
            content = loader.load_data(source)
        elif source_type == 'url':
            loader = UrlLoader()
            content = loader.load_data(source)
        elif source_type == 'text':
            content = source  # For text, the source is the content itself
        else:
            raise ValueError("Unsupported source type. Please use 'pdf', 'url', or 'text'.")

        parser = PydanticOutputParser(pydantic_object=MCQList)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            Generate {num} multiple-choice questions based on the given content.
            Content: {topic}

            For each question, provide:
            1. The question
            2. A list of options (including the correct answer)
            3. The correct answer
            4. An explanation (optional)

            Learning Objective: {learning_objective}
            Difficulty Level: {difficulty_level}

            Ensure that the questions are relevant to the learning objective and match the specified difficulty level.

            The response should be in JSON format.
            {format_instructions}
            """

        mcq_prompt = PromptTemplate(
            input_variables=["num", "topic", "learning_objective", "difficulty_level"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        mcq_chain = mcq_prompt | self.llm

        results = mcq_chain.invoke({
            "num": num,
            "topic": content,
            "learning_objective": learning_objective,
            "difficulty_level": difficulty_level,
            **kwargs
        })
        results = results.content

        try:
            structured_output = parser.parse(results)
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results)
            return MCQList(questions=[])

    def generate_questions_from_youtube(self, url: str, num: int = 1, question_type: str = "Multiple Choice", prompt_template: Optional[str] = None, custom_instructions: Optional[str] = None, **kwargs) -> QuestionList:
        transcript = self.get_youtube_transcript(url)

        questions = self.generate_questions(
            topic=transcript,
            num=num,
            type=question_type,
            prompt_template=prompt_template,
            custom_instructions=custom_instructions,
            **kwargs
        )

        return questions

    @staticmethod
    def get_youtube_transcript(url: str) -> str:
        try:
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
            transcript = loader.load()
            return transcript
        except Exception as e:
            raise ValueError(f"Error fetching transcript: {str(e)}")

class AdaptiveQuiz:
    def __init__(self, config: EduchainConfig, qna_engine: QnAEngine, topic: str, num_questions: int = 5, custom_instruction: str = "", show_options: bool = False, data: Optional[str] = None, source_type: Optional[str] = None, difficulty_level: str = "Medium"):
        self.config = config
        self.qna_engine = qna_engine
        self.topic = topic
        self.num_questions = num_questions
        self.custom_instruction = custom_instruction
        self.show_options = show_options
        self.data = data
        self.source_type = source_type
        self.quiz_data = []
        self.start_time = None
        self.difficulty_level = difficulty_level
        custom_template = """
        Generate {num} multiple-choice question (MCQ) based on the given topic and level.
        Provide the question, four answer options, and the correct answer.

        Topic: {topic}
        Learning Objective: {learning_objective}
        Difficulty Level: {difficulty_level}
        """

        adaptive_template = """
        Based on the user's response to the previous question on {topic}, generate a new multiple-choice question (MCQ).
        If the user's response is correct, output a harder question. Otherwise, output an easier question.
        Provide the question, four answer options, and the correct answer.

        Previous Question: {previous_question}
        User's Response: {user_response}
        Was the response correct?: {response_correct}
        """

        def __init__(self, db=None, llm=None, difficulty_level="Medium", topic="", num_questions=5, custom_instruction="", show_options=False, data=None, source_type=None):
            self.db = db
            self.llm = llm or self.initialize_llm()
            self.difficulty_level = difficulty_level
            self.topic = topic
            self.num_questions = num_questions
            self.custom_instruction = custom_instruction
            self.quiz_data = []
            self.start_time = None
            self.show_options = show_options
            self.data = data
            self.source_type = source_type

            self.supabase = None
            if db == "supabase":
                self.supabase = self.initialize_supabase()

    @staticmethod
    def initialize_llm():
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI Key not found in environment variables.")
        return ChatOpenAI(
            model="gpt-4o-mini",
            #openai_api_base="https://api.groq.com/openai/v1",
            openai_api_key=api_key
        )

    @staticmethod
    def initialize_supabase():
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Supabase URL or Key not found in environment variables.")
        return create_client(url, key)

    def generate_initial_question(self):
        if self.data:
            result = self.qna_engine.generate_mcqs_from_data(
                source=self.data,
                source_type=self.source_type,
                num=1,
                difficulty_level=self.difficulty_level
            )
        else:
            result = self.qna_engine.generate_mcq(
                topic=self.topic,
                num=1,
                custom_instructions=f"General knowledge of {self.topic}",
                difficulty_level=self.difficulty_level
            )
        return result.questions[0] if result and result.questions else None

    def generate_next_question(self, previous_question, user_response, response_correct):
        if self.data:
            result = self.qna_engine.generate_mcqs_from_data(
                source=self.data,
                source_type=self.source_type,
                num=1,
            )
        else:
            result = self.qna_engine.generate_mcq(
                topic=self.topic,
                num=1,
                custom_instructions=f"Based on the user's response to the previous question on {self.topic}, generate a new multiple-choice question (MCQ). If the user's response is correct, output a harder question. Otherwise, output an easier question. Previous Question: {previous_question}, User's Response: {user_response}, Was the response correct?: {response_correct}"
            )
        return result.questions[0] if result and result.questions else None

    def start_quiz(self):
        self.start_time = time.time()
        question_number = 0
        score = 0

        current_question = self.generate_initial_question()
        while question_number < self.num_questions and current_question:
            print(f"Question {question_number + 1}: {current_question.question}")
            if self.show_options:
                for i, option in enumerate(current_question.options):
                    print(f"{i+1}. {option}")
                user_answer = input("Select the correct option number: ")
                user_answer = current_question.options[int(user_answer) - 1]
            else:
                user_answer = input("Your answer: ")
            correct_answer = current_question.answer

            if user_answer == correct_answer:
                print("Correct!")
                score += 1
                response_correct = "True"
            else:
                print(f"Incorrect. The correct answer was {correct_answer}.")
                response_correct = "False"

            # Log quiz data
            self.quiz_data.append({
                "question_number": question_number + 1,
                "question": current_question.question,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "response_correct": response_correct,
            })

            # Generate the next question
            question_number += 1
            current_question = self.generate_next_question(
                current_question.question,
                user_answer,
                response_correct
            )

        total_time = time.time() - self.start_time
        print(f"Quiz completed! Final Score: {score}/{self.num_questions}. Total Time: {total_time:.2f} seconds")

        if self.supabase:
            self.save_to_supabase(score, total_time)

    def save_to_supabase(self, score, total_time):
        try:
            data = {
                "topic": self.topic,
                "difficulty_increase_threshold": self.difficulty_increase_threshold,
                "num_questions": self.num_questions,
                "score": score,
                "total_time": total_time,
                "quiz_data": self.quiz_data
            }
            print(data)
            response = self.supabase.table("quiz_results").insert(data).execute()
            if response.status_code != 201:
                raise Exception(f"Failed to save quiz data to Supabase. Response: {response.data}")
            print("Quiz data successfully saved to Supabase.")
        except Exception as e:
            print(f"An error occurred while saving to Supabase: {e}")



        # Implement the rest of the AdaptiveQuiz methods (start_quiz, generate_initial_question, generate_next_question, etc.)
        # Similar to the current implementation, but use self.qna_engine for generating questions
