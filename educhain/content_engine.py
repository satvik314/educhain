from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from .models import LessonPlan,QuestionPaper
from typing import List, Optional


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
