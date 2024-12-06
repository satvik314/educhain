import sys
from educhain.core.config import LLMConfig
from educhain.engines.content_engine import ContentEngine

def test_generate_lesson_plan():
    try:
        
        llm_config = LLMConfig(
            model_name="gpt-4o",
            api_key="",
            max_tokens=4000,
            temperature=0.5,
        )

        content_engine = ContentEngine(llm_config=llm_config)

        topic = "Linear Algebra"

        custom_instructions = "Focus on hands-on activities and real-world examples."

        # Generate the lesson plan
        lesson_plan = content_engine.generate_lesson_plan(
            topic=topic,
            custom_instructions=custom_instructions,
            output_format="csv"
        )

        # Display the lesson plan using the show() function
        print(lesson_plan)
        lesson_plan.show()

    except Exception as e:
        print(f"Error generating lesson plan: {e}")

# Run the test
if __name__ == "__main__":
    test_generate_lesson_plan()
