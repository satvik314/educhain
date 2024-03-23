from typing import List
from langchain_core.pydantic_v1 import BaseModel

class Question(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

class Quiz(BaseModel):
    questions: List[Question]