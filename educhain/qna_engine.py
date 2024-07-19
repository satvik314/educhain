import json
from .utils import to_csv, to_json, to_pdf  ###
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from .models import MCQList ###
from .models import *


def generate_mcq(topic, num=1, llm=None, response_model=None, prompt_template=None, custom_instructions=None, **kwargs):
    if response_model == None:
        parser = PydanticOutputParser(pydantic_object=MCQList)
        format_instructions = parser.get_format_instructions()
    else:
        parser = PydanticOutputParser(pydantic_object=response_model)
        format_instructions = parser.get_format_instructions()

    if prompt_template is None:
        prompt_template = """
        Generate {num} multiple-choice question (MCQ) based on the given topic and level.
        provide the question, four answer options, and the correct answer.

        Topic: {topic}
        """

    # Add custom instructions if provided
    if custom_instructions:
        prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

    # Append the JSON format instruction line to the custom prompt template
    prompt_template += "\nThe response should be in JSON format. \n {format_instructions}"

    MCQ_prompt = PromptTemplate(
        input_variables=["num", "topic"],
        template=prompt_template,
        partial_variables={"format_instructions": format_instructions}
    )

    if llm:
        llm = llm
    else:
        llm = ChatOpenAI(model="gpt-4o-mini")

    MCQ_chain = MCQ_prompt | llm

    results = MCQ_chain.invoke(
        {"num": num, "topic": topic, **kwargs},
    )

    results = results.content
    structured_output = parser.parse(results)

    return structured_output

QuestionType = Literal["Multiple Choice", "Short Answer", "True/False", "Fill in the Blank"]

def generate_questions(
    topic: str,
    num: int = 1,
    llm: Optional[Any] = None,
    type: QuestionType = "Multiple Choice",
    prompt_template: Optional[str] = None,
    custom_instructions: Optional[str] = None,
    **kwargs
) -> QuestionList:
    if type == "Multiple Choice":
        parser = PydanticOutputParser(pydantic_object=MCQList)
    elif type == "Short Answer":
        parser = PydanticOutputParser(pydantic_object=ShortAnswerQuestionList)
    elif type == "True/False":
        parser = PydanticOutputParser(pydantic_object=TrueFalseQuestionList)
    elif type == "Fill in the Blank":
        parser = PydanticOutputParser(pydantic_object=FillInBlankQuestionList)
    else:
        raise ValueError(f"Unsupported question type: {type}")

    format_instructions = parser.get_format_instructions()

    if prompt_template is None:
        prompt_template = f"""
        Generate {{num}} {type} question(s) based on the given topic.
        Topic: {{topic}}

        For each question, provide:
        1. The question
        2. The correct answer
        3. An explanation (optional)
        """

        if type == "Multiple Choice":
            prompt_template += "\n4. A list of options (including the correct answer)"
        elif type == "Short Answer":
            prompt_template += "\n4. A list of relevant keywords"
        elif type == "True/False":
            prompt_template += "\n4. The correct answer as a boolean (true/false)"
        elif type == "Fill in the Blank":
            prompt_template += "\n4. The word or phrase to be filled in the blank"

    if custom_instructions:
        prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

    prompt_template += "\n\nThe response should be in JSON format.\n{format_instructions}"

    question_prompt = PromptTemplate(
        input_variables=["num", "topic"],
        template=prompt_template,
        partial_variables={"format_instructions": format_instructions}
    )

    if llm is None:
        llm = ChatOpenAI(model="gpt-4o-mini")

    question_chain = question_prompt | llm
    results = question_chain.invoke(
        {"num": num, "topic": topic, **kwargs},
    )
    results = results.content

    try:
        # Parse the JSON manually
        # import json
        # parsed_json = json.loads(results)

        # if type == "Fill in the Blank":
        #     # For Fill in the Blank, set blank_word to answer if not provided
        #     for q in parsed_json['questions']:
        #         if 'blank_word' not in q:
        #             q['blank_word'] = q['answer']

        # Now use the parser with the modified JSON
        # structured_output = parser.parse(json.dumps(parsed_json))
        structured_output = parser.parse(results)
        return structured_output
    except Exception as e:
        print(f"Error parsing output: {e}")
        print("Raw output:")
        print(results)
        return QuestionList(questions=[])

def generate_mcqs_from_data(
    source: str,
    source_type: str,
    num: int = 1,
    llm: Optional[ChatOpenAI] = None,
    learning_objective: str = "",
    difficulty_level: str = "",
    prompt_template: Optional[str] = None,
    **kwargs
) -> MCQList:
    # Load data based on source type
    if source_type == 'pdf':
        loader = PdfFileLoader()
        content = loader.load_data(source)
    elif source_type == 'url':
        loader = UrlLoader()
        content = loader.load_data(source)
    elif source_type == 'text':
        content = source  # For text, the source is the content itself
    else:
        raise ValueError("Unsupported source type. Please use 'pdf', 'url', or 'text'.")

    # Set up the parser
    parser = PydanticOutputParser(pydantic_object=MCQList)
    format_instructions = parser.get_format_instructions()

    # Set up the prompt template
    if prompt_template is None:
        prompt_template = """
        Generate {num} multiple-choice questions based on the given content.
        Content: {topic}

        For each question, provide:
        1. The question
        2. A list of options (including the correct answer)
        3. The correct answer
        4. An explanation (optional)

        Learning Objective: {learning_objective}
        Difficulty Level: {difficulty_level}

        Ensure that the questions are relevant to the learning objective and match the specified difficulty level.

        The response should be in JSON format.
        {format_instructions}
        """

    # Create the prompt
    mcq_prompt = PromptTemplate(
        input_variables=["num", "topic", "learning_objective", "difficulty_level"],
        template=prompt_template,
        partial_variables={"format_instructions": format_instructions}
    )

    # Set up the language model
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o-mini")

    # Create the chain
    mcq_chain = mcq_prompt | llm

    # Generate MCQs
    results = mcq_chain.invoke({
        "num": num,
        "topic": content,
        "learning_objective": learning_objective,
        "difficulty_level": difficulty_level,
        **kwargs
    })
    results = results.content

    try:
        # Parse the JSON manually
        parsed_json = json.loads(results)
        
        # Now use the parser with the parsed JSON
        # structured_output = parser.parse(json.dumps(parsed_json))
        structured_output = parser.parse(results)
        return structured_output
    except Exception as e:
        print(f"Error parsing output: {e}")
        print("Raw output:")
        print(results)
        return MCQList(questions=[])
