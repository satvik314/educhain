from .utils import to_csv, to_json, to_pdf  ###
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from .models import MCQList ###

def generate_mcq(topic, level, num=1, custom_template="", llm=None, **kwargs):
    parser = PydanticOutputParser(pydantic_object=MCQList)
    format_instructions = parser.get_format_instructions()

    prompt_template = """
    Generate {num} multiple-choice question (MCQ) based on the given topic and level.
    provide the question, four answer options, and the correct answer.

    Topic: {topic}
    Level: {level}
    
    {custom_template}
    
    The response should be in JSON format. \n {format_instructions}
    """

    MCQ_prompt = PromptTemplate(
        input_variables=["num", "topic", "level", "custom_template"],
        template=prompt_template,
        partial_variables={"format_instructions": format_instructions}
    )

    if llm:
        llm = llm
    else:
        llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    MCQ_chain = LLMChain(llm=llm, prompt=MCQ_prompt)

    results = MCQ_chain.invoke(
        {"num": num, "topic": topic, "level": level, "custom_template": custom_template, **kwargs},
        return_only_outputs=True
    )

    results = results["text"]
    structured_output = parser.parse(results)

    return structured_output
