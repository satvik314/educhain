import hashlib
#import fitz  # PyMuPDF for handling PDF files
import re
import requests
from bs4 import BeautifulSoup
from typing import List, Optional, Dict, Any, Literal
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
import os
import json
from PyPDF2 import PdfReader


# Pydantic models
class BaseQuestion(BaseModel):
    question: str
    answer: str
    explanation: Optional[str] = None

    def show(self):
        print(f"Question: {self.question}")
        print(f"Answer: {self.answer}")
        if self.explanation:
            print(f"Explanation: {self.explanation}")
        print()

class MultipleChoiceQuestion(BaseQuestion):
    options: List[str]

    def show(self):
        print(f"Question: {self.question}")
        options_str = "\n".join(f"  {chr(65 + i)}. {option}" for i, option in enumerate(self.options))
        print(f"Options:\n{options_str}")
        print(f"\nCorrect Answer: {self.answer}")
        if self.explanation:
            print(f"Explanation: {self.explanation}")
        print()

class ShortAnswerQuestion(BaseQuestion):
    keywords: List[str] = Field(default_factory=list)

    def show(self):
        super().show()
        if self.keywords:
            print(f"Keywords: {', '.join(self.keywords)}")
        print()

class TrueFalseQuestion(BaseQuestion):
    answer: bool

    def show(self):
        super().show()
        print(f"True/False: {self.answer}")
        print()

class FillInBlankQuestion(BaseQuestion):
    blank_word: Optional[str] = None

    def show(self):
        super().show()
        print(f"Word to fill: {self.blank_word or self.answer}")
        print()

class QuestionList(BaseModel):
    questions: List[BaseQuestion]

    def show(self):
        for i, question in enumerate(self.questions, 1):
            print(f"Question {i}:")
            question.show()

class MCQList(QuestionList):
    questions: List[MultipleChoiceQuestion]

class ShortAnswerQuestionList(QuestionList):
    questions: List[ShortAnswerQuestion]

class TrueFalseQuestionList(QuestionList):
    questions: List[TrueFalseQuestion]

class FillInBlankQuestionList(QuestionList):
    questions: List[FillInBlankQuestion]

class MCQ(MultipleChoiceQuestion):
    """A class representing a multiple choice question."""
    correct_answer: str

    def show(self):
        super().show()
        print(f"Correct Answer: {self.correct_answer}")
        print()

class LessonPlan(BaseModel):
    """A class representing a lesson plan."""
    topic: str
    objectives: List[str]
    introduction: str
    content: str
    assessment: str
    conclusion: str

    def show(self):
        print(f"Topic: {self.topic}")
        print("Objectives:")
        for objective in self.objectives:
            print(f"- {objective}")
        print(f"Introduction: {self.introduction}")
        print(f"Content: {self.content}")
        print(f"Assessment: {self.assessment}")
        print(f"Conclusion: {self.conclusion}\n")

class QuestionPaper(BaseModel):
    """A class representing a question paper."""
    subject: str
    grade_level: int
    num_questions: int
    question_types: List[str]
    time_limit: Optional[int]
    difficulty_level: Optional[str]
    topics: Optional[List[str]]
    questions: List[BaseQuestion]

    def show(self):
        print(f"Subject: {self.subject}")
        print(f"Grade Level: {self.grade_level}")
        print(f"Number of Questions: {self.num_questions}")
        print(f"Question Types: {', '.join(self.question_types)}")
        print(f"Time Limit: {self.time_limit} minutes" if self.time_limit else "No time limit")
        print(f"Difficulty Level: {self.difficulty_level}" if self.difficulty_level else "Not specified")
        print(f"Topics: {', '.join(self.topics)}" if self.topics else "Not specified")
        print("\nQuestions:")
        for i, question in enumerate(self.questions, 1):
            print(f"Question {i}:")
            question.show()


# Loader classes
class PdfFileLoader:
    def load_data(self, file_path):
        reader = PdfReader(file_path)
        all_content = []

        for page in reader.pages:
            content = page.extract_text()
            content = self.clean_string(content)
            all_content.append(content)

        return " ".join(all_content)

    def clean_string(self, text):
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

class UrlLoader:
    def load_data(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.get_text()
        return self.clean_string(content)

    def clean_string(self, text):
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
# Vision Doubt Solving
class LLMConfig(BaseModel):
    model_name: str
    api_key_name: str
    max_tokens: int = 1000

class DoubtSolverConfig(BaseModel):
    gpt4: LLMConfig = LLMConfig(model_name="gpt-4o-mini", api_key_name="OPENAI_API_KEY")

class SolvedDoubt(BaseModel):
    explanation: str
    steps: Optional[List[str]] = Field(default_factory=list)
    additional_notes: Optional[str] = None

    def show(self):
        print("Explanation:")
        print(self.explanation)
        print("\nSteps:")
        for i, step in enumerate(self.steps, 1):
            print(f"{i}. {step}")
        if self.additional_notes:
            print("\nAdditional Notes:")
            print(self.additional_notes)
