from educhain.models.base_models import BaseQuestion, QuestionList
from pydantic import BaseModel, Field
from typing import List, Optional

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

class MCQList(QuestionList):
    questions: List[MultipleChoiceQuestion]

class ShortAnswerQuestionList(QuestionList):
    questions: List[ShortAnswerQuestion]

class TrueFalseQuestionList(QuestionList):
    questions: List[TrueFalseQuestion]

class FillInBlankQuestionList(QuestionList):
    questions: List[FillInBlankQuestion]

class Option(BaseModel):
    text: str = Field(description="The text of the option.")
    correct: str = Field(description="Whether the option is correct or not. Either 'true' or 'false'")

class MCQMath(BaseModel):
    question: str = Field(description="The quiz question, strictly avoid Latex formatting")
    requires_math: bool = Field(default=False, description="Whether the question requires the LLM Math Chain for accurate answers.")
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