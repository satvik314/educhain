from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from langchain_community.document_loaders import YoutubeLoader
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import re


class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: Optional[str] = None
    
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

class TrueFalseQuestion(BaseQuestion):
    answer: bool

class FillInBlankQuestion(BaseQuestion):
    blank_word: Optional[str] = None

class QuestionList(BaseModel):
    questions: List[BaseQuestion]

class MCQList(BaseModel):
    questions: List[MCQ] = Field(default_factory=list)

class ShortAnswerQuestionList(QuestionList):
    questions: List[ShortAnswerQuestion]

class TrueFalseQuestionList(QuestionList):
    questions: List[TrueFalseQuestion]

class FillInBlankQuestionList(QuestionList):
    questions: List[FillInBlankQuestion]

class LessonPlan(BaseModel):
    topic: str
    objectives: List[str]
    introduction: str
    content: str
    assessment: str
    conclusion: str

class QuestionPaper(BaseModel):
    subject: str
    grade_level: int
    num_questions: int
    question_types: List[str]
    time_limit: Optional[int]
    difficulty_level: Optional[str]
    topics: Optional[List[str]]
    questions: List[BaseQuestion]

class DoubtSolverConfig(BaseModel):
    model_name: str = "gpt-4o-mini"
    api_key_name: str = "OPENAI_API_KEY"
    max_tokens: int = 1000

class SolvedDoubt(BaseModel):
    explanation: str
    steps: Optional[List[str]] = Field(default_factory=list)
    additional_notes: Optional[str] = None

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
