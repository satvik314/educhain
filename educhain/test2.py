from pydantic import BaseModel, Field
from typing import List, Dict, Any
import json
import os
from pathlib import Path
from dotenv import load_dotenv
# from educhain import Educhain
from engines.qna_engine import QnAEngine
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
# Define your Topics Data in Json Format
client = QnAEngine()

class Option(BaseModel):
    text: str = Field(description="The text of the option")
    correct: bool = Field(description="Whether this option is correct")

class DataSufficiencyQuestion(BaseModel):
    question_text: str = Field(description="The text of the question")
    statement_1: str = Field(description="Statement 1")
    statement_2: str = Field(description="Statement 2")
    options: List[Option] = Field(description="List of options for the question")
    explanation: str = Field(description="Explanation of the correct answer")
    metadata: Dict[str, Any] = Field(description="Additional metadata including section, subsection, topic, and subtopic.")
    difficulty_level: str = Field(description="Difficulty level of the question (e.g., Easy, Medium, Hard)")
    difficulty_rating: float = Field(description="Difficulty rating of the question (e.g., 3.5/5)")
    estimated_time: int = Field(description="Estimated time to solve the question in seconds")

class DataSufficiencyQuestionList(BaseModel):
    questions: List[DataSufficiencyQuestion] = Field(description="List of Data Sufficiency questions")

# GMAT Data Sufficiency Prompt Template
GMAT_DATA_SUFFICIENCY_PROMPT_TEMPLATE = """
Generate {num} GMAT-style Data Sufficiency questions following these specifications:

Section: Data Insights
Subsection: Data Sufficiency
Topic: Arithmetic DS
Subtopic: {subtopic}
Difficulty: {difficulty_level} (Easy, Medium, Hard)

**Learning Objectives:**
{learning_objective}

**Question Format Requirements:**
1. Ensure the question is clear and concise.
2. Include all necessary information for solving the problem.
3. Provide two statements (Statement 1 and Statement 2) to evaluate sufficiency.
4. Ensure the difficulty level matches the specified value (Easy, Medium, Hard).
5. Provide a difficulty rating (e.g., 3.5/5) based on the complexity of the question.
6. Provide an estimated time to solve the question in seconds:
   - Easy: 60-90 seconds
   - Medium: 120-150 seconds
   - Hard: 180-210 seconds
7. Ensure that no two questions follow the same pattern or structure.
8. Questions should mimic the style and complexity of real GMAT questions.

**Important Notes:**
- Avoid generating variations of the same question (e.g., changing only numbers or variables).
- Ensure diversity in question patterns by varying the operations, contexts, and problem structures.
- For **Easy** questions, focus on basic concepts and straightforward calculations.
- For **Medium** questions, include multi-step problems or require application of concepts.
- For **Hard** questions, incorporate complex problem-solving, abstract reasoning, or real-world scenarios.

The response MUST return a list of questions in the following JSON format:
{{
  "questions": [
    {{
      "question_text": "Clear question statement",
      "statement_1": "First statement",
      "statement_2": "Second statement",
      "options": [
        {{
          "text": "Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.",
          "correct": true/false
        }},
        {{
          "text": "Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.",
          "correct": true/false
        }},
        {{
          "text": "BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.",
          "correct": true/false
        }},
        {{
          "text": "EACH statement ALONE is sufficient.",
          "correct": true/false
        }},
        {{
          "text": "Statements (1) and (2) TOGETHER are NOT sufficient.",
          "correct": true/false
        }}
      ],
      "explanation": "Detailed explanation of why the selected option is correct",
      "metadata": {{
        "section": "Data Insights",
        "subsection": "Data Sufficiency",
        "topic": "Arithmetic DS",
        "subtopic": "{subtopic}"
      }},
      "difficulty_level": "Easy/Medium/Hard",
      "difficulty_rating": 3.5,
      "estimated_time": 90
    }}
  ]
}}
"""

# Example topic structure for GMAT Data Sufficiency
topics_data = [
    {
        "topic": "Arithmetic DS",
        "subtopics": [
            {
                "name": "Fractions (DS)",
                "learning_objectives": [
                    "Understand how to interpret and manipulate fractions in data sufficiency problems.",
                    "Solve GMAT-style data sufficiency problems involving fraction operations.",
                    "Analyze data sufficiency questions to determine if the given information is sufficient to solve problems involving fractions."
                ]
            },
            {
                "name": "Decimals (DS)",
                "learning_objectives": [
                    "Understand how to interpret and manipulate decimals in data sufficiency problems.",
                    "Solve GMAT-style data sufficiency problems involving decimal operations.",
                    "Analyze data sufficiency questions to determine if the given information is sufficient to solve problems involving decimals."
                ]
            }
        ]
    }
]

client = QnAEngine()

# Save topics data to a JSON file
topics_file = "gmat_ds_topics.json"
with open(topics_file, "w") as f:
    json.dump(topics_data, f, indent=2)

# Generate questions using bulk generation
result, output_file, total_generated, failed_batches = client.bulk_generate_questions(
    topic=topics_file,
    total_questions=10,
    # questions_per_objective=5,
    max_workers=5,
    output_format="pdf",
    max_retries=3,
    prompt_template=GMAT_DATA_SUFFICIENCY_PROMPT_TEMPLATE,
    question_model=DataSufficiencyQuestion,
    question_list_model=DataSufficiencyQuestionList,
    difficulty_level="Medium"
)
print(f"\nGeneration completed!")
result.model_dump()