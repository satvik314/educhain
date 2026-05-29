"""
Prompt builders for the QnA engine.

With the OpenAI SDK the response schema is enforced by the structured-output
machinery in :class:`~educhain.core.client.LLMClient`, so prompts only need to
describe the *task* - they no longer carry hand-written "format instructions".
"""

from __future__ import annotations

from typing import Optional

QUESTION_SYSTEM_PROMPT = (
    "You are an expert educational content creator. You write clear, accurate, "
    "pedagogically sound assessment questions and always ground them in the "
    "given topic or source material."
)

# Type-specific guidance appended to the base question prompt.
_TYPE_GUIDANCE = {
    "Multiple Choice": (
        "Provide 4 options, exactly one of which is correct. Set 'answer' to the "
        "text of the correct option."
    ),
    "Short Answer": (
        "Provide a concise text answer (not options) and a list of relevant "
        "keywords that a good answer should contain."
    ),
    "True/False": (
        "The statement must be unambiguously true or false. Set 'answer' to the "
        "boolean value."
    ),
    "Fill in the Blank": (
        "Write the question with a blank shown as '_____'. Set 'answer' (and "
        "'blank_word') to the word or phrase that fills the blank."
    ),
}


def question_prompt(
    topic: str,
    num: int,
    question_type: str = "Multiple Choice",
    custom_template: Optional[str] = None,
    custom_instructions: Optional[str] = None,
    **context,
) -> str:
    """Build the prompt for ``QnAEngine.generate``."""
    if custom_template:
        base = custom_template
    else:
        base = (
            f"Generate {num} {question_type} question(s) based on the given topic.\n"
            f"Topic: {topic}\n\n"
            "For each question, provide the question text, the correct answer, "
            "and a brief explanation.\n"
            f"{_TYPE_GUIDANCE.get(question_type, '')}"
        )

    for key, value in context.items():
        if value:
            base += f"\n{key.replace('_', ' ').title()}: {value}"

    if custom_instructions:
        base += f"\n\nAdditional instructions:\n{custom_instructions}"
    return base


MATH_SYSTEM_PROMPT = (
    "You are an academic AI assistant specialised in mathematics. You create "
    "computation-based multiple-choice questions with unambiguous numerical "
    "answers."
)


def math_prompt(topic: str, num: int, custom_instructions: Optional[str] = None) -> str:
    base = (
        f"Generate {num} multiple-choice questions that require mathematical "
        f"computation, based on the topic: {topic}.\n\n"
        "For each question:\n"
        "1. Make sure it requires a real calculation.\n"
        "2. Set requires_math to true.\n"
        "3. Provide four distinct numerical options.\n"
        "4. Mark the single correct option.\n"
        "5. Give a step-by-step explanation."
    )
    if custom_instructions:
        base += f"\n\nAdditional instructions:\n{custom_instructions}"
    return base


VISUAL_SYSTEM_PROMPT = (
    "You are an expert at writing quantitative questions that are answered by "
    "reading a chart or table."
)

VISUAL_PROMPT_TEMPLATE = """Generate exactly {num} quantitative questions based on the topic: {topic}.

Each question must require a visual representation of data (bar, pie, line, scatter, or table) to answer. Choose the visual type based on the data:
- pie: proportions / parts of a whole
- bar: comparing discrete categories or frequency distributions
- line: change over time or relationship between continuous variables
- scatter: relationship between two continuous variables
- table: exact numerical data in rows and columns

For each question provide: the question text, four options, the correct answer, an explanation, and a graph_instruction object describing how to draw the visual. The graph_instruction must include the relevant keys for its type:
- type: one of "bar", "pie", "line", "scatter", "table"
- bar/line: x_labels, y_values, y_label, title (use a list of lists for y_values + labels for multiple lines)
- scatter: x_values, y_values, y_label, title
- pie: labels, sizes, title
- table: data (a list of row objects), title

The question must be solvable purely from the data shown in the visual."""


def visual_prompt(topic: str, num: int, custom_instructions: Optional[str] = None) -> str:
    base = VISUAL_PROMPT_TEMPLATE.format(num=num, topic=topic)
    if custom_instructions:
        base += f"\n\nAdditional instructions:\n{custom_instructions}"
    return base


DOUBT_SYSTEM_PROMPT = (
    "You are a helpful tutor that explains how to solve problems shown in "
    "images. You respond clearly, using Markdown, with step-by-step reasoning."
)


def rag_prompt(
    num: int,
    question_type: str,
    context: str,
    learning_objective: Optional[str] = None,
    difficulty_level: Optional[str] = None,
    custom_instructions: Optional[str] = None,
) -> str:
    """Build the prompt for retrieval-augmented question generation."""
    base = (
        f"Using ONLY the reference material below, generate {num} {question_type} "
        f"question(s).\n\n"
        f"{_TYPE_GUIDANCE.get(question_type, '')}\n"
    )
    if learning_objective:
        base += f"\nLearning objective: {learning_objective}"
    if difficulty_level:
        base += f"\nDifficulty level: {difficulty_level}"
    if custom_instructions:
        base += f"\nAdditional instructions: {custom_instructions}"
    base += f"\n\n--- Reference material ---\n{context}\n--- End reference material ---"
    return base


__all__ = [
    "QUESTION_SYSTEM_PROMPT",
    "MATH_SYSTEM_PROMPT",
    "VISUAL_SYSTEM_PROMPT",
    "DOUBT_SYSTEM_PROMPT",
    "question_prompt",
    "math_prompt",
    "visual_prompt",
    "rag_prompt",
]
