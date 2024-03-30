from typing import List
from langchain_core.pydantic_v1 import BaseModel

class MCQ(BaseModel):
    """A class representing a multiple choice question."""
    question: str
    options: List[str]
    correct_answer: str
    
    def show(self):
        options_str = "\n".join(f"  {chr(65 + i)}. {option}" for i, option in enumerate(self.options))
        print(f"Question: {self.question}\nOptions:\n{options_str}\nCorrect Answer: {self.correct_answer}\n")




class MCQList(BaseModel):
    questions: List[MCQ]

    def show(self):
        print("MCQs:\n")
        for i, mcq in enumerate(self.questions):
            print(f"Question {i + 1}:")
            mcq.show()