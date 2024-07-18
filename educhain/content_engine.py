from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from .models import LessonPlan,QuestionPaper , DoubtSolverConfig, SolvedDoubt
from typing import List, Optional ,Any 
from langchain.schema import HumanMessage, SystemMessage
import os
import base64

def generate_lesson_plan(topic, llm=None, response_model=None, prompt_template=None, **kwargs):
    if response_model == None:
        parser = PydanticOutputParser(pydantic_object=LessonPlan)
        format_instructions = parser.get_format_instructions()
    else:
        parser = PydanticOutputParser(pydantic_object=response_model)
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

    # Append the JSON format instruction line to the custom prompt template
    prompt_template += "\nThe response should be in JSON format. \n {format_instructions}"

    lesson_plan_prompt = PromptTemplate(
        input_variables=["topic"],
        template=prompt_template,
        partial_variables={"format_instructions": format_instructions}
    )

    if llm:
        llm = llm
    else:
        llm = ChatOpenAI(model="gpt-3.5-turbo")

    lesson_plan_chain = lesson_plan_prompt | llm

    results = lesson_plan_chain.invoke(
        {"topic": topic, **kwargs},
    )
    results = results.content
    structured_output = parser.parse(results)
    return structured_output

def generate_question_paper(
    subject: str,
    grade_level: int,
    num_questions: int,
    question_types: List[str] = ['multiple_choice'],
    time_limit: Optional[int] = None,
    difficulty_level: Optional[str] = None,
    topics: Optional[List[str]] = None,
    llm=None,
    response_model=None,
    prompt_template=None,
    **kwargs
):
    if response_model is None:
        parser = PydanticOutputParser(pydantic_object=QuestionPaper)
        format_instructions = parser.get_format_instructions()
    else:
        parser = PydanticOutputParser(pydantic_object=response_model)
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

    if llm:
        llm = llm
    else:
        llm = ChatOpenAI(model="gpt-3.5-turbo")

    QP_chain = QP_prompt | llm

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

# Vision Class
class DoubtSolver:
    def __init__(self, config: DoubtSolverConfig = DoubtSolverConfig()):
        self.config = config

    def solve(self, 
              img_path: str, 
              prompt: str = "Explain how to solve this problem", 
              llm: Optional[Any] = None,
              custom_instructions: Optional[str] = None,
              **kwargs) -> Optional[SolvedDoubt]:
        
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

        if llm is None:
            llm = self._get_chat_model()

        try:
            response = llm([system_message, human_message])
            result = parser.parse(response.content)
            return result
        except Exception as e:
            print(f"Error in solve: {type(e).__name__}: {str(e)}")
            return None

    def _get_chat_model(self) -> ChatOpenAI:
        config = self.config.gpt4
        return ChatOpenAI(
            model_name=config.model_name, 
            api_key=os.getenv(config.api_key_name), 
            max_tokens=config.max_tokens,
            temperature=0,
        )

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
