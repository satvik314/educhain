import json
from .utils import to_csv  # Import the to_csv function from the utils module
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from .models import MCQList, MCQ
    
def generate_mcq(topic, level = "Intermediate", num = 1, llm = ChatOpenAI(), file_name=None):

    parser = PydanticOutputParser(pydantic_object=MCQList)

    format_instructions = parser.get_format_instructions()

    MCQ_template = """
    Generate {num} multiple-choice question (MCQ) based on the given topic and level.
    provide the question, four answer options, and the correct answer.

    Topic: {topic}
    Level: {level}

    The response should be in JSON format. \n {format_instructions}
    """

    MCQ_prompt = PromptTemplate(input_variables=["num", "topic", "level"],
                                template=MCQ_template,
                                partial_variables={"format_instructions": format_instructions}
                                )

    MCQ_chain = LLMChain(llm=llm, prompt=MCQ_prompt)
    results = MCQ_chain.invoke({"num": num,
                                    "topic": topic,
                                    "level": level
                                    }, return_only_outputs=True)

    results = results["text"]
    structured_output = parser.parse(results)
    
    # Generate Csv file if file_name is provided
    if file_name:
        to_csv(structured_output, file_name)
        
    return structured_output
