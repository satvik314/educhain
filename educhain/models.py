from typing import List
from langchain_core.pydantic_v1 import BaseModel

class Question(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

    def __str__(self):
        options_str = "\n".join(f"  - {option}" for option in self.options)
        return f"Question: {self.question}\nOptions:\n{options_str}\nCorrect Answer: {self.correct_answer}"

class Quiz(BaseModel):
    questions: List[Question]