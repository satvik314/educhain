from educhain.engines.content_engine import ContentEngine
from educhain.core.config import LLMConfig

def test_generate_career_connections():
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
        topic = "Data Science"
        industry_focus = "Technology"

        # Generate the career connections
        print(f"\nGenerating career connections for: {topic}")
        print(f"Industry Focus: {industry_focus}")
        
        career_connections = content_engine.generate_career_connections(
            topic=topic,
            industry_focus=industry_focus,
            output_format="csv"
        )

        career_connections.show()  # Using the show method we defined in the Pydantic model

    except Exception as e:
        print(f"\nError generating career connections: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_generate_career_connections()