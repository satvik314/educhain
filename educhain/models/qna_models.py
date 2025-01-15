from educhain.models.base_models import BaseQuestion, QuestionList
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, field_validator

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

class SolvedDoubt(BaseModel):
    """Model for representing a solved doubt with explanation and steps"""
    explanation: str = Field(
        description="Detailed explanation of the problem and its solution"
    )
    steps: List[str] = Field(
        default_factory=list,
        description="Step-by-step solution process"
    )
    additional_notes: Optional[str] = Field(
        default=None,
        description="Additional tips, warnings, or relevant information"
    )

    def show(self):
        """Display the solved doubt in a formatted way"""
        print("\n=== Problem Explanation ===")
        print(self.explanation)
        
        if self.steps:
            print("\n=== Solution Steps ===")
            for i, step in enumerate(self.steps, 1):
                print(f"{i}. {step}")
        
        if self.additional_notes:
            print("\n=== Additional Notes ===")
            print(self.additional_notes)

class SpeechInstructions(BaseModel):
    topic: str
    num_questions: Optional[int] = 5
    custom_instructions: Optional[str] = None
    detected_language: Optional[str] = "english"


class GraphInstructions(BaseModel):
    """Pydantic model for graph instructions"""
    type: Literal["bar", "line", "pie", "scatter", "table"] = Field(..., description="The type of graph (bar, line, pie, scatter, table).")
    x_labels: Optional[List[str]] = Field(None, description="Labels for the x-axis (bar, line, scatter).")
    y_values: Optional[List[float]] = Field(None, description="Data points for the y-axis (bar, line, scatter).")
    labels: Optional[List[str]] = Field(None, description="Labels for the pie chart.")
    sizes: Optional[List[float]] = Field(None, description="Sizes for the pie chart.")
    data: Optional[List[Dict[str, Any]]] = Field(None, description="Data points for table.")
    y_label: Optional[str] = Field(None, description="Label for the y-axis (bar, line, scatter).")
    title: str = Field(..., description="Title of the graph or table.")
    x_values: Optional[List[float]] = Field(None, description="X Values for scatter plot")


class GMATQuestion(BaseModel):
    """Pydantic model for a GMAT visual question."""
    question_text: str = Field(..., description="The text of the question.")
    options: List[str] = Field(..., description="Options for the multiple choice question.")
    graph_instruction: GraphInstructions = Field(..., description="Instructions for how to generate the graph or table.")
    correct_answer: str = Field(..., description="The correct answer")

    @field_validator("graph_instruction", mode='before')
    def validate_graph_instructions(cls, value):
        if isinstance(value, dict):
          return GraphInstructions(**value)
        return value

class GMATQuestionList(BaseModel):
      questions: List[GMATQuestion]