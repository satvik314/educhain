from pydantic import BaseModel, Field
from typing import List, Optional

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

class QuestionList(BaseModel):
    questions: List[BaseQuestion]

    def show(self):
        for i, question in enumerate(self.questions, 1):
            print(f"Question {i}:")
            question.show()