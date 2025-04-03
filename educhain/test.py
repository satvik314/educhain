from langchain_openai import ChatOpenAI
from engines.qna_engine import QnAEngine
from dotenv import load_dotenv
import json
import os

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
# Define your Topics Data in Json Format
client = QnAEngine()
example_topics_data = [
    {
        "topic": "Mathematics",
        "subtopics": [
            {
                "name": "Fractions",
                "learning_objectives": [
                    "Convert proper fractions to improper fractions and mixed numbers",
                    "Add and subtract fractions with like denominators",
                    "Find equivalent fractions using multiplication and division"
                ]
            },
        ]
    }
]

topic_json_path = "topics.json"

# Save example data to file
with open(topic_json_path, 'w') as f:
  json.dump(example_topics_data, f, indent=4)

# Generate questions with total questions specified
result, output_file, total_generated, failed_batches = client.bulk_generate_questions(
        topic=topic_json_path,
        total_questions=10,
        # questions_per_objective=10,
        max_workers=5,
        output_format="pdf",
        max_retries=2,
        difficulty="medium"
    )

print(f"\nGeneration completed!")