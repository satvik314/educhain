import sys
from educhain.core.config import LLMConfig
from educhain.engines.qna_engine import QnAEngine

def test_question_generation():
    try:
        
        llm_config = LLMConfig(
            model_name="gpt-4o",
            api_key="",
            max_tokens=4000,
            temperature=0.5,
        )

        qna_engine = QnAEngine(llm_config=llm_config)

        topic = "Gravitation"
        num = 5
        question_type = "Multiple Choice"

        # Generate the lesson plan
        qna = qna_engine.generate_questions(
            topic=topic,
            num=num,
            question_type=question_type,
            output_format="csv"
        )

        # Display the lesson plan using the show() function
        print(qna)

    except Exception as e:
        print(f"Error generating questions: {e}")

# Run the test
if __name__ == "__main__":
    test_question_generation()
