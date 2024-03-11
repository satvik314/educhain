from langchain_openai import ChatOpenAI
from langchain import PromptTemplate, LLMChain


def generate_mcq(topic, level, llm = ChatOpenAI()):

    prompt = PromptTemplate(
        input_variables=["topic", "level"],
        template="""
    Generate a multiple-choice question (MCQ) based on the given topic and level.
    Provide the question, four answer options, and the correct answer.

    Topic: {topic}
    Level: {level}

    Question:
    """,
    )

    # Create an LLMChain using the prompt and ChatOpenAI
    mcq_chain = LLMChain(llm=llm, prompt=prompt)

    # Generate the MCQ
    mcq = mcq_chain.run(topic=topic, level=level)

    return mcq

    



