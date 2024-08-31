#Experiments
import json
from .utils import to_csv, to_json, to_pdf
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, LLMMathChain
from langchain.output_parsers import PydanticOutputParser
from .models import MCQList
from .models import *
from langchain_community.document_loaders import YoutubeLoader
import time
from qna_engine import generate_mcq,generate_questions,generate_mcqs_from_data,generate_questions_from_youtube
from typing import List, Dict, Any, Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.callbacks.manager import get_openai_callback
import random


class Adaptive_Quiz:

    custom_template = """
    Generate {num} multiple-choice question (MCQ) based on the given topic and level.
    Provide the question, four answer options, and the correct answer.

    Topic: {topic}
    Learning Objective: {learning_objective}
    Difficulty Level: {difficulty_level}
    """

    adaptive_template = """
    Based on the user's response to the previous question on {topic}, generate a new multiple-choice question (MCQ).
    If the user's response is correct, output a harder question. Otherwise, output an easier question.
    Provide the question, four answer options, and the correct answer.

    Previous Question: {previous_question}
    User's Response: {user_response}
    Was the response correct?: {response_correct}
    """

    def __init__(self, db=None, llm=None, difficulty_increase_threshold="Medium", topic="", num_questions=5, custom_instruction="", show_options=False, data=None, source_type=None):
        self.db = db
        self.llm = llm or self.initialize_llm()
        self.difficulty_increase_threshold = difficulty_increase_threshold
        self.topic = topic
        self.num_questions = num_questions
        self.custom_instruction = custom_instruction
        self.quiz_data = []
        self.start_time = None
        self.show_options = show_options
        self.data = data
        self.source_type = source_type

        self.supabase = None
        if db == "supabase":
            self.supabase = self.initialize_supabase()

    @staticmethod
    def initialize_llm():
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI Key not found in environment variables.")
        return ChatOpenAI(
            model="gpt-4o-mini",
            #openai_api_base="https://api.groq.com/openai/v1",
            openai_api_key=api_key
        )

    @staticmethod
    def initialize_supabase():
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Supabase URL or Key not found in environment variables.")
        return create_client(url, key)

    def generate_initial_question(self):
        if self.data:
            result = generate_mcqs_from_data(
                source=self.data,
                source_type=self.source_type,
                num=1,
                llm=self.llm,
            )
        else:
            result = generate_mcq(
                topic=self.topic,
                num=1,
                learning_objective=f"General knowledge of {self.topic}",
                difficulty_level=self.difficulty_increase_threshold,
                llm=self.llm,
                prompt_template=self.custom_template,  # Use self.custom_template
            )
        return result.questions[0] if result and result.questions else None

    def generate_next_question(self, previous_question, user_response, response_correct):
        if self.data:
            result = generate_mcqs_from_data(
                source=self.data,
                source_type=self.source_type,
                num=1,
                llm=self.llm,
            )
        else:
            result = generate_mcq(
                topic=self.topic,
                num=1,
                llm=self.llm,
                prompt_template=self.adaptive_template,  # Use self.adaptive_template
                previous_question=previous_question,
                user_response=user_response,
                response_correct=response_correct
            )
        return result.questions[0] if result and result.questions else None

    def start_quiz(self):
        self.start_time = time.time()
        question_number = 0
        score = 0

        current_question = self.generate_initial_question()
        while question_number < self.num_questions and current_question:
            print(f"Question {question_number + 1}: {current_question.question}")
            if self.show_options:
                for i, option in enumerate(current_question.options):
                    print(f"{i+1}. {option}")
                user_answer = input("Select the correct option number: ")
                user_answer = current_question.options[int(user_answer) - 1]
            else:
                user_answer = input("Your answer: ")
            correct_answer = current_question.answer

            if user_answer == correct_answer:
                print("Correct!")
                score += 1
                response_correct = "True"
            else:
                print(f"Incorrect. The correct answer was {correct_answer}.")
                response_correct = "False"

            # Log quiz data
            self.quiz_data.append({
                "question_number": question_number + 1,
                "question": current_question.question,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "response_correct": response_correct,
            })

            # Generate the next question
            question_number += 1
            current_question = self.generate_next_question(
                current_question.question,
                user_answer,
                response_correct
            )

        total_time = time.time() - self.start_time
        print(f"Quiz completed! Final Score: {score}/{self.num_questions}. Total Time: {total_time:.2f} seconds")

        if self.supabase:
            self.save_to_supabase(score, total_time)

    def save_to_supabase(self, score, total_time):
        try:
            data = {
                "topic": self.topic,
                "difficulty_increase_threshold": self.difficulty_increase_threshold,
                "num_questions": self.num_questions,
                "score": score,
                "total_time": total_time,
                "quiz_data": self.quiz_data
            }
            print(data)
            response = self.supabase.table("quiz_results").insert(data).execute()
            if response.status_code != 201:
                raise Exception(f"Failed to save quiz data to Supabase. Response: {response.data}")
            print("Quiz data successfully saved to Supabase.")
        except Exception as e:
            print(f"An error occurred while saving to Supabase: {e}")






#qna_engine_math________________________________________________


#MODEL
class Option(BaseModel):
    text: str = Field(description="The text of the option.")
    correct: str = Field(description="Whether the option is correct or not. Either 'true' or 'false'")

class MCQMath(BaseModel):
    question: str = Field(description="The quiz question, strictly avoid Latex formatting")
    requires_math: bool = Field(default=False, description="""Whether the question requires the LLM Math Chain for accurate answers. This includes, but is not limited to: 
    1. Any arithmetic operations (addition, subtraction, multiplication, division)
    2. Calculations involving percentages
    3. Problems with exponents or roots
    4. Logarithmic calculations
    5. Trigonometric functions
    6. Algebraic equations or expressions
    7. Statistical calculations (mean, median, mode, standard deviation, etc.)
    8. Probability calculations
    9. Series or sequence calculations
    10. Calculus-related problems (derivatives, integrals)
    11. Geometry problems involving area, volume, or angles
    12. Unit conversions
    13. Financial calculations (compound interest, depreciation, etc.)
    14. Any problem involving multiple steps of mathematical reasoning
    15. Sorting or ranking based on numerical values
    16. Optimization problems
    17. Any question that explicitly asks for a numerical answer
    Set to True if any of these conditions are met, ensuring the LLM Math Chain is utilized for all questions requiring precise mathematical computations.""")
    # requires_math: bool = Field(default=False, description="Whether the question requires help from LLM_Math or has advanced math calculations. Questions which has multiplication, division, sorting, exponents, etc.")
    options: List[Option] = Field(description="The possible answers to the question. The list should contain 4 options.")
    explanation: str =  Field(default=None, description="Explanation of the question")

    def show(self):
      print(f"Question: {self.question}")
      for i, option in enumerate(self.options):
            print(f"  {chr(65 + i)}. {option.text} {'(Correct)' if option.correct == 'true' else ''}")
      if self.explanation:
          print(f"Explanation: {self.explanation}")
      print()

class MCQListMath(BaseModel):
    questions: List[MCQMath]

    def show(self):
      for i, question in enumerate(self.questions, 1):
          print(f"Question {i}:")
          question.show()


# FUNCTIONS:

# GENERATE SIMILAR OTPIONS:
def generate_similar_options(question, correct_answer, num_options=3):
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)
    prompt = f"Generate {num_options} incorrect but plausible options similar to this correct answer: {correct_answer} for this question: {question}. Provide only the options, separated by semicolons. The options should not precede or end with any symbols, it should be similar to the correct answer."
    response = llm.predict(prompt)
    return response.split(';')


# MAIN GENERATE MCQ FUNCTION:
def generate_mcq_math(topic, num=1, llm=None, response_model=None, prompt_template=None, custom_instructions=None, **kwargs):
    if response_model == None:
        parser = PydanticOutputParser(pydantic_object=MCQListMath)
        format_instructions = parser.get_format_instructions()
    else:
        parser = PydanticOutputParser(pydantic_object=response_model)
        format_instructions = parser.get_format_instructions()

    if prompt_template is None:
        prompt_template = """
        You are an Academic AI assistant tasked with generating multiple-choice questions on various topics specialised in Maths Subject.
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

    # Initialize LLMMathChain
    llm_math = LLMMathChain.from_llm(llm=llm, verbose=False)

    # Process questions that contain math expressions
    for question in structured_output.questions:
        if question.requires_math:
            try:
                # Use LLMMathChain to solve the question
                with get_openai_callback() as cb:
                    result = llm_math.run(question.question)
                    result = result.strip().split(":")[-1]
                    result = float(result)
                    result = f"{result: .2f}"

                # Update the question's explanation with the math solution
                question.explanation += f"\n\nMath solution: {result}"

                # Generate new options based on the LLMMathChain result
                correct_option = Option(text=str(result.lstrip()), correct='true')
                incorrect_options = [Option(text=opt.strip(), correct='false') for opt in generate_similar_options(question.question, result)]

                # Ensure we have exactly 4 options
                while len(incorrect_options) < 3:
                    incorrect_options.append(Option(text="N/A", correct='false'))

                question.options = [correct_option] + incorrect_options[:3]
                random.shuffle(question.options) 
            except Exception as e:
                print(f"LLMMathChain failed to answer: {str(e)}")
                # If LLMMathChain fails, keep the original options
                pass
    return structured_output


