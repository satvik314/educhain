from educhain import Educhain , LLMConfig
from typing import Any, Dict
import logging
from dotenv import load_dotenv
load_dotenv()


logger = logging.getLogger(__name__)
custom_config = LLMConfig(model_name="gpt-4o")

# Initialize the Educhain client with the custom configuration
client = Educhain(custom_config)
#client = Educhain()  # Global client

def generate_content(topic: str, pedagogy: str, params: Dict[str, Any]) -> Any:
    try:
        # Ensure params is a dictionary
        if not isinstance(params, dict):
            params = {}
        
        # Add default values for all pedagogy parameters
        default_params = get_default_params(pedagogy)
        for key, default_value in default_params.items():
            if not params.get(key):
                params[key] = default_value
        
        logger.info(f"Generating content for {pedagogy} with topic '{topic}' and params: {params}")
        
        result = client.content_engine.generate_pedagogy_content(
            topic=topic,
            pedagogy=pedagogy,
            **params
        )
        
        logger.info(f"Generated content result: {result}")
        return result
    except Exception as e:
        logger.error(f"Educhain error: {e}")
        raise

def get_default_params(pedagogy: str) -> Dict[str, str]:
    """Get default parameters for each pedagogy"""
    defaults = {
        "blooms_taxonomy": {
            "grade_level": "High School",
            "target_level": "Intermediate"
        },
        "socratic_questioning": {
            "depth_level": "Intermediate",
            "student_level": "High School"
        },
        "project_based_learning": {
            "project_duration": "4-6 weeks",
            "team_size": "3-4 students",
            "industry_focus": "General"
        },
        "flipped_classroom": {
            "class_duration": "50 minutes",
            "prep_time": "30-45 minutes",
            "technology_level": "Moderate"
        },
        "inquiry_based_learning": {
            "inquiry_type": "Guided",
            "investigation_scope": "Moderate",
            "student_autonomy": "Balanced"
        },
        "constructivist": {
            "prior_knowledge_level": "Mixed",
            "social_interaction_focus": "High",
            "reflection_emphasis": "Strong"
        },
        "gamification": {
            "game_mechanics": "Points, badges, levels",
            "competition_level": "Moderate",
            "technology_platform": "Web-based"
        },
        "peer_learning": {
            "group_size": "3-4 students",
            "collaboration_type": "Mixed",
            "skill_diversity": "Moderate"
        }
    }
    return defaults.get(pedagogy, {})
        

def get_pedagogies() -> Dict[str, Dict[str, Any]]:
    try:
        return client.content_engine.get_available_pedagogies()
    except Exception as e:
        logger.error(f"Failed to fetch pedagogies: {e}")
        raise
