from typing import List, Optional, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from .models import LessonPlan, QuestionPaper, DoubtSolverConfig, SolvedDoubt
from .config import EduchainConfig
from langchain.schema import HumanMessage, SystemMessage
import os
import base64

class ContentEngine:
    def __init__(self, config: EduchainConfig):
        self.config = config
        self.llm = self._initialize_llm()

    def _initialize_llm(self) -> ChatOpenAI:
        llm_config = self.config.llm_config
        return ChatOpenAI(
            model_name=llm_config.model_name,
            openai_api_key=llm_config.api_key,  # Changed from api_key_name to api_key
            max_tokens=llm_config.max_tokens
        )

    def generate_lesson_plan(self, topic: str, prompt_template: Optional[str] = None, **kwargs) -> LessonPlan:
        parser = PydanticOutputParser(pydantic_object=LessonPlan)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            Generate a comprehensive lesson plan for the given topic and duration.
            Include the following details in the lesson plan:
            - Objectives: List the learning objectives of the lesson.
            - Introduction: Provide an engaging introduction to the lesson.
            - Content Outline: Outline the main points or sections of the lecture content.
            - Assessment: Describe how the students' understanding will be assessed.
            - Conclusion: Summarize the key takeaways and provide a conclusion for the lesson.

            Topic: {topic}
            """

        prompt_template += "\nThe response should be in JSON format. \n {format_instructions}"

        lesson_plan_prompt = PromptTemplate(
            input_variables=["topic"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        lesson_plan_chain = lesson_plan_prompt | self.llm

        results = lesson_plan_chain.invoke(
            {"topic": topic, **kwargs},
        )
        results = results.content
        structured_output = parser.parse(results)
        return structured_output

    def generate_question_paper(self, subject: str, grade_level: int, num_questions: int, question_types: List[str] = ['multiple_choice'], time_limit: Optional[int] = None, difficulty_level: Optional[str] = None, topics: Optional[List[str]] = None, prompt_template: Optional[str] = None, **kwargs) -> QuestionPaper:
        parser = PydanticOutputParser(pydantic_object=QuestionPaper)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            Generate a {num_questions}-question multiple-choice {subject} assessment for grade {grade_level}.
            
            The assessment should have a time limit of {time_limit} minutes if provided, and a difficulty level of {difficulty_level} if provided.
            The assessment should cover the following topics if provided: {topics}
            
            The response should be in JSON format.
            {format_instructions}
            """

        QP_prompt = PromptTemplate(
            input_variables=["subject", "grade_level", "num_questions", "time_limit", "difficulty_level", "topics"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        QP_chain = QP_prompt | self.llm

        results = QP_chain.invoke(
            {
                "subject": subject,
                "grade_level": grade_level,
                "num_questions": num_questions,
                "question_types": question_types,
                "time_limit": time_limit,
                "difficulty_level": difficulty_level,
                "topics": topics,
                **kwargs
            }
        )

        structured_output = parser.parse(results.content)
        return structured_output

class DoubtSolver:
    def __init__(self, config: EduchainConfig, doubt_solver_config: DoubtSolverConfig = DoubtSolverConfig()):
        self.config = config
        self.doubt_solver_config = doubt_solver_config
        self.llm = self._initialize_llm()

    def _initialize_llm(self) -> ChatOpenAI:
        return ChatOpenAI(
            model_name=self.doubt_solver_config.model_name,
            openai_api_key=os.getenv(self.doubt_solver_config.api_key_name),
            max_tokens=self.doubt_solver_config.max_tokens,
            temperature=0,
        )

    def solve(self, img_path: str, prompt: str = "Explain how to solve this problem", custom_instructions: Optional[str] = None, **kwargs) -> Optional[SolvedDoubt]:
        if not img_path:
            raise ValueError("Image path or URL is required")

        image_content = self._get_image_content(img_path)
        
        parser = PydanticOutputParser(pydantic_object=SolvedDoubt)
        format_instructions = parser.get_format_instructions()

        system_message = SystemMessage(content="You are a helpful assistant that responds in Markdown. Help with math homework.")

        human_message_content = f"""
        Analyze the image and {prompt}
        
        Provide:
        1. A detailed explanation
        2. Step-by-step solution (if applicable)
        3. Any additional notes or tips
        
        {custom_instructions or ''}
        
        {format_instructions}
        """

        human_message = HumanMessage(content=[
            {"type": "text", "text": human_message_content},
            {"type": "image_url", "image_url": {"url": image_content}}
        ])

        try:
            response = self.llm([system_message, human_message])
            result = parser.parse(response.content)
            return result
        except Exception as e:
            print(f"Error in solve: {type(e).__name__}: {str(e)}")
            return None

    @staticmethod
    def _get_image_content(img_path: str) -> str:
        try:
            if img_path.startswith(('http://', 'https://')):
                return img_path
            elif img_path.startswith('data:image'):
                return img_path
            elif os.path.isfile(img_path):
                with open(img_path, "rb") as image_file:
                    image_data = image_file.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
                return f"data:image/jpeg;base64,{base64_image}"
            else:
                raise ValueError("Invalid image path or URL")
        except Exception as e:
            print(f"Error in _get_image_content: {type(e).__name__}: {str(e)}")
            raise
