# in educhain/models/qna_models.py
from educhain.models.base_models import BaseQuestion, QuestionList
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

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

# Add these new models:
class GraphInstruction(BaseModel):
    type: str = Field(..., description="Type of visualization (bar, pie, line, scatter, table)")
    x_labels: Optional[List[str]] = Field(None, description="Labels for x-axis (for bar, line)")
    x_values: Optional[List[Any]] = Field(None, description="Values for x-axis (for scatter)")
    y_values: Optional[List[Any]] = Field(None, description="Values for y-axis (for bar, line, scatter, multiple lines in line)")
    labels: Optional[List[str]] = Field(None, description="Labels for pie chart segments or line graph legend")
    sizes: Optional[List[float]] = Field(None, description="Sizes for pie chart segments")
    y_label: Optional[str] = Field(None, description="Label for y-axis")
    title: Optional[str] = Field(None, description="Title of the visualization")
    data: Optional[List[Dict[str, Any]]] = Field(None, description="Data for table visualization")


class VisualMCQ(MultipleChoiceQuestion):
    graph_instruction: Optional[GraphInstruction] = Field(None, description="Instructions for generating a graph")

    def show(self):
        super().show()
        if self.graph_instruction:
            print(f"Graph Instruction: {self.graph_instruction}")
        print()

class VisualMCQList(QuestionList):
    questions: List[VisualMCQ]


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

class BulkMCQ(BaseModel):
    question: str = Field(description="The quiz question, strictly avoid Latex formatting")
    options: List[Option] = Field(description="The possible answers to the question. The list should contain 4 options.")
    explanation: str = Field(default=None, description="Explanation of the correct answer")
    difficulty: str = Field(description="The difficulty level of the question (easy, medium, hard)")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata including topic, subtopic, and learning objective"
    )

class BulkMCQList(BaseModel):
    questions: List[BulkMCQ]

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


class SanityCheckResult(BaseModel):
    question: str = Field(..., description="The question being evaluated")
    answer: str = Field(..., description="The correct answer")
    options: Optional[List[str]] = Field(None, description="Options if MCQ, else None")
    keywords: Optional[List[str]] = Field(None, description="Keywords if Short Answer, else None")
    answer_correctness: str = Field(..., description="Correct or Incorrect")
    question_clarity: str = Field(..., description="Clear and Correct or Needs Improvement")
    distractor_plausibility: str = Field(..., description="Plausible Distractors, Implausible Distractors, or N/A")
    passed: bool = Field(..., description="Whether the question passed the sanity check")

class SanityCheckSummary(BaseModel):
    results: List[SanityCheckResult] = Field(..., description="List of individual sanity check results")
    total_questions: int = Field(..., description="Total number of questions checked")
    passed_questions: int = Field(..., description="Number of questions that passed")
    failed_questions: int = Field(..., description="Number of questions that failed")

    def show(self):
        print("=" * 80)
        print(f"Sanity Check Summary")
        print(f"Total Questions: {self.total_questions}")
        print(f"Passed: {self.passed_questions} | Failed: {self.failed_questions}")
        print("=" * 80)
        for i, result in enumerate(self.results, 1):
            print(f"\nQuestion {i}: {result.question}")
            print(f"Answer: {result.answer}")
            if result.options:
                print("Options:")
                for j, opt in enumerate(result.options):
                    print(f"  {chr(65+j)}. {opt}")
            if result.keywords:
                print(f"Keywords: {', '.join(result.keywords)}")
            print(f"Answer Correctness: {result.answer_correctness}")
            print(f"Question Clarity: {result.question_clarity}")
            print(f"Distractor Plausibility: {result.distractor_plausibility}")
            print(f"Result: {'Passed' if result.passed else 'Failed'}")
        print("=" * 80)
