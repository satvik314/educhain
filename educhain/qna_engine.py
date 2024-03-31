from .utils import to_csv, to_json, to_pdf  # Import the to_csv and to_json function from the utils module ###
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from .models import Quiz  ###
    
def generate_mcq(topic, level, num = 1, model='gpt-3.5-turbo', temperature=0.7):

    try:
        parser = PydanticOutputParser(pydantic_object=Quiz)
        
        llm = ChatOpenAI(model=model, temperature=temperature)

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
            
        return structured_output
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
