from typing import List, Optional
from langchain_core.pydantic_v1 import BaseModel

class MCQ(BaseModel):
    """A class representing a multiple choice question."""
    question: str
    options: List[str]
    correct_answer: str
    explanation: str
    
    def show(self):
        options_str = "\n".join(f"  {chr(65 + i)}. {option}" for i, option in enumerate(self.options))
        print(f"Question: {self.question}\nOptions:\n{options_str}\nCorrect Answer: {self.correct_answer}\nExplanation: {self.explanation}\n")


class MCQList(BaseModel):
    questions: List[MCQ]

    def show(self):
        print("MCQs:\n")
        for i, mcq in enumerate(self.questions):
            print(f"Question {i + 1}:")
            mcq.show()

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
    questions: List[MCQ]

    def show(self):
        print(f"Subject: {self.subject}")
        print(f"Grade Level: {self.grade_level}")
        print(f"Number of Questions: {self.num_questions}")
        print(f"Question Types: {', '.join(self.question_types)}")
        print(f"Time Limit: {self.time_limit} minutes" if self.time_limit else "No time limit")
        print(f"Difficulty Level: {self.difficulty_level}" if self.difficulty_level else "Not specified")
        print(f"Topics: {', '.join(self.topics)}" if self.topics else "Not specified")
        print("\nQuestions:")
        for i, mcq in enumerate(self.questions):
            print(f"Question {i + 1}:")
            mcq.show()
