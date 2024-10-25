from educhain.engines.content_engine import ContentEngine
from educhain.core.config import LLMConfig

def test_generate_study_guide():
    try:
        # Initialize LLM configuration
        llm_config = LLMConfig(
            model_name="gpt-4o",
            api_key="",
            max_tokens=4000,
            temperature=0.5,
        )

        # Initialize content engine
        content_engine = ContentEngine(llm_config=llm_config)

        # Test parameters
        topic = "Ethical Hacking"
        difficulty_level = "Beginner"
        custom_instructions = """
        Include hands-on examples and some real-world techniques.
        Focus on practical applications and security best practices.
        """

        # Generate the study guide
        print(f"\nGenerating study guide for: {topic}")
        study_guide = content_engine.generate_study_guide(
            topic=topic,
            difficulty_level=difficulty_level,
            custom_instructions=custom_instructions,
        )

        # Display results
        print("\nGenerated Study Guide:")
        print("-" * 50)
        study_guide.show(format="text")  # Using the new format parameter

    except Exception as e:
        print(f"\nError generating study guide: {e}")

if __name__ == "__main__":
    test_generate_study_guide()