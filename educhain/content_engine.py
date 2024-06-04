from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from .models import LessonPlan

def generate_lesson_plan(topic, duration, llm=None, response_model=None, prompt_template=None, **kwargs):
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
        - Prerequisites: Specify any prior knowledge or skills required for the lesson.
        - Introduction: Provide an engaging introduction to the lesson.
        - Content Outline: Outline the main points or sections of the lecture content.
        - Assessment: Describe how the students' understanding will be assessed.
        - Conclusion: Summarize the key takeaways and provide a conclusion for the lesson.

        Topic: {topic}
        Duration: {duration}
        """

    # Append the JSON format instruction line to the custom prompt template
    prompt_template += "\nThe response should be in JSON format. \n {format_instructions}"

    lesson_plan_prompt = PromptTemplate(
        input_variables=["topic", "duration"],
        template=prompt_template,
        partial_variables={"format_instructions": format_instructions}
    )

    if llm:
        llm = llm
    else:
        llm = ChatOpenAI(model="gpt-3.5-turbo")

    lesson_plan_chain = lesson_plan_prompt | llm

    results = lesson_plan_chain.invoke(
        {"topic": topic, "duration": duration, **kwargs},
    )
    results = results.content
    structured_output = parser.parse(results)
    return structured_output