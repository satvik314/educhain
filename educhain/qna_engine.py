import json
from .utils import to_csv, to_json, to_pdf  ###
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from .models import MCQList ###



def generate_mcq(topic, level, num=1, llm=None, response_model=None , prompt_template=None, **kwargs):

    if response_model == None:
      parser = PydanticOutputParser(pydantic_object = MCQList)
      format_instructions = parser.get_format_instructions()
    else:
      parser = PydanticOutputParser(pydantic_object = response_model)
      format_instructions = parser.get_format_instructions()

    if prompt_template is None:
        prompt_template = """
        Generate {num} multiple-choice question (MCQ) based on the given topic and level.
        provide the question, four answer options, and the correct answer.

        Topic: {topic}
        Level: {level}
        """

    # Append the JSON format instruction line to the custom prompt template
    prompt_template += "\nThe response should be in JSON format. \n {format_instructions}"

    MCQ_prompt = PromptTemplate(
        input_variables=["num", "topic", "level"],
        template=prompt_template,
        partial_variables={"format_instructions": format_instructions}
    )

    if llm:
        llm = llm
    else:
        llm = ChatOpenAI(model="gpt-3.5-turbo")

    # MCQ_chain = LLMChain(llm=llm, prompt=MCQ_prompt)
    MCQ_chain = MCQ_prompt | llm

    results = MCQ_chain.invoke(
        {"num": num, "topic": topic, "level": level, **kwargs},
        # return_only_outputs=True

    )

    results = results.content
    structured_output = parser.parse(results)

