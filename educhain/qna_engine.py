import json
from utils import to_csv  # Import the to_csv function from the utils module
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain import PromptTemplate, LLMChain

load_dotenv()

def generate_mcq(topic, level, num = 1, model='gpt-3.5-turbo', temperature=0.7, file_name=None):

    try:
        llm = ChatOpenAI(model=model, temperature=temperature)

        MCQ_template = """
        Generate {num} multiple-choice question (MCQ) based on the given topic and level.
        provide the question, four answer options, and the correct answer.

        Topic: {topic}
        Level: {level}

        The response should be in JSON format.
        The JSON should contain the following fields:
        - question: The question.
        - options: An array of four answer options.
        - correct_answer: The correct answer.
        """

        MCQ_prompt = PromptTemplate(input_variables=["num", "topic", "level"],
                                    template=MCQ_template
                                    )

        MCQ_chain = LLMChain(llm=llm, prompt=MCQ_prompt)
        results_str = MCQ_chain.run({"num": num,
                                     "topic": topic,
                                     "level": level
                                     })

        result = json.loads(results_str)

        # Generate Csv file if file_name is provided
        if file_name:
            to_csv(result, file_name, num)

        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    