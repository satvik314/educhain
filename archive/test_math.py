from educhain.core.config import LLMConfig
from engines.qna_engine import QnAEngine  
# Step 1: Initialize the engine
llm_config = LLMConfig(
    api_key="",  # Replace with your actual OpenAI API key
    model_name="gpt-4o-mini",  # Or use any model you have access to
    temperature=0.7,
    max_tokens=500
)

engine = QnAEngine(llm_config=llm_config)

# Step 2: Define the topic for math questions
topic = "Basic Algebra"

# Step 3: Generate MCQ Math questions
num_questions = 3  # Number of questions you want to generate
response = engine.generate_mcq_math(
    topic=topic,
    num=num_questions
)

print(response)

# Step 4: Output the result
print("Generated MCQ Math Questions:")
for question in response.questions:
    print(f"Question: {question.question}")
    print("Options:")
    for option in question.options:
        print(f" - {option.text} {'(Correct)' if option.correct == 'true' else ''}")
    print(f"Explanation: {question.explanation}\n")
