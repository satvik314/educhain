from typing import Optional, Type, Any
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from educhain.core.config import LLMConfig
from educhain.models.content_models import LessonPlan, StudyGuide

class ContentEngine:
    def __init__(self, llm_config: Optional[LLMConfig] = None):
        if llm_config is None:
            llm_config = LLMConfig()
        self.llm = self._initialize_llm(llm_config)

    def _initialize_llm(self, llm_config: LLMConfig):
        if llm_config.custom_model:
            return llm_config.custom_model
        else:
            return ChatOpenAI(
                model=llm_config.model_name,
                api_key=llm_config.api_key,
                max_tokens=llm_config.max_tokens,
                temperature=llm_config.temperature,
                base_url=llm_config.base_url,
                default_headers=llm_config.default_headers
            )

    # Lesson Plan
    def generate_lesson_plan(
        self,
        topic: str,
        grade_level: Optional[str] = None,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        llm: Optional[Any] = None,
        **kwargs
    ) -> Any:
        if response_model is None:
            response_model = LessonPlan

        parser = PydanticOutputParser(pydantic_object=response_model)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            Create a highly engaging and comprehensive lesson plan for the following topic:
            Topic: {topic}

            The lesson plan should be structured in a way that engages students through a variety of methods.
            The structure should include the following elements:
            1. Title of the lesson
            2. Subject area
            3. Learning objectives (at least 3, tailored to different learning levels or grades)
            4. Lesson introduction (including a hook to grab attention, real-world applications, or provocative questions)
            5. Main topics (2-3), each should include:
                a. Title
                b. Subtopics (2-3)
                c. For each subtopic:
                    - Key Concepts (definitions, examples, illustrations, multimedia)
                    - Discussion Questions (to encourage critical thinking and engagement)
                    - Hands-on Activities or Project-Based Learning (interactive, real-world tasks)
                    - Reflective Questions (to evaluate understanding)
                    - Assessment Ideas (quiz, project, or written task to assess mastery)
            6. Learning adaptations for different grade levels (if applicable)
            7. A section on real-world applications, including careers and future learning paths
            8. Ethical considerations and societal impact (if applicable)

            Ensure that the lesson plan follows Bloom's Taxonomy principles with activities addressing different cognitive levels: remember, understand, apply, analyze, evaluate, and create.

            The lesson plan should cater to diverse learning styles (visual, auditory, kinesthetic, etc.) and include modern teaching methods such as collaborative learning and technology integration.

            Output the response in a structured and professional format.

            Response format: 
            {format_instructions}
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\n\n{format_instructions}"

        lesson_plan_prompt = PromptTemplate(
            input_variables=["topic"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        llm_to_use = llm if llm is not None else self.llm

        # Use LLM to generate lesson plan based on the topic
        lesson_plan_chain = lesson_plan_prompt | llm_to_use
        results = lesson_plan_chain.invoke(
            {"topic": topic, **kwargs},
        )
        results = results.content

        # Print raw output for debugging
        print("Raw output from LLM:")
        print(results)

        try:
            # Parse results to match the new LessonPlan structure
            structured_output = parser.parse(results)
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results)
            return response_model()
        
    # Study Guide
    def generate_study_guide(
        self,
        topic: str,
        difficulty_level: Optional[str] = None,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        llm: Optional[Any] = None,
        **kwargs
    ) -> Any:
        if response_model is None:
            response_model = StudyGuide

        parser = PydanticOutputParser(pydantic_object=response_model)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            Create a comprehensive study guide for the following topic:
            Topic: {topic}
            Difficulty Level: {difficulty_level}

            The study guide should be engaging, well-structured, and suitable for self-study or classroom use.
            Include the following elements in your response:

            1. Difficulty level and estimated study time
            2. Prerequisites (if any)
            3. Clear learning objectives (3-5 specific, measurable objectives)
            4. Comprehensive overview of the topic
            5. Key concepts with detailed explanations
            6. Important dates and events (if applicable)
            8. Practice exercises formatted as:
            "practice_exercises": [
                {{
                    "title": "Exercise Title",
                    "problem": "Detailed problem description",
                    "solution": "Step-by-step solution",
                    "difficulty": "beginner|intermediate|advanced"
                }}
            ]
            9. Real-world case studies formatted as:
            "case_studies": [
                {{
                    "title": "Case Study Title",
                    "scenario": "Description of the real-world situation",
                    "challenge": "Specific problems or challenges faced",
                    "solution": "How the challenges were addressed",
                    "outcome": "Results and impact",
                    "lessons_learned": ["Key lesson 1", "Key lesson 2"],
                    "related_concepts": ["Concept 1", "Concept 2"]
                }}
            ]
            10. Study tips and strategies specific to the topic
            11. Additional resources for deeper learning
            12. Brief summary of key takeaways

            For the case studies:
            - Include at least one detailed real-world example
            - Focus on recent and relevant scenarios
            - Highlight practical applications of the concepts
            - Connect the case study to specific learning objectives
            - Emphasize problem-solving approaches
            - Include both successes and lessons learned
            - Make sure the examples are appropriate for the difficulty level

            Make sure all content is hands-on and directly related to real-world applications of {topic}.
            The study guide should accommodate different learning styles and include various types of learning activities.
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\n\nThe response should be in JSON format.\n{format_instructions}"

        study_guide_prompt = PromptTemplate(
            input_variables=["topic", "difficulty_level"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        llm_to_use = llm if llm is not None else self.llm

        study_guide_chain = study_guide_prompt | llm_to_use
        results = study_guide_chain.invoke(
            {
                "topic": topic,
                "difficulty_level": difficulty_level or "Intermediate",
                **kwargs
            },
        )
        results = results.content

        try:
            # Handle empty practice exercises
            if '"practice_exercises": []' in results or '"practice_exercises":[]' in results:
                results = results.replace(
                    '"practice_exercises": []',
                    '"practice_exercises": [{"title": "Basic Exercise", "problem": "No exercises provided", "solution": "N/A", "difficulty": "beginner"}]'
                )
                
            # Handle empty case studies
            if '"case_studies": []' in results or '"case_studies":[]' in results:
                results = results.replace(
                    '"case_studies": []',
                    '"case_studies": [{"title": "Sample Case", "scenario": "No case studies provided", "challenge": "N/A", "solution": "N/A", "outcome": "N/A", "lessons_learned": ["N/A"], "related_concepts": ["N/A"]}]'
                )
                
            structured_output = parser.parse(results)
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results)
            # Return an instance with default values including case studies
            return response_model(
                topic=topic,
                overview="Error generating content",
                key_concepts={"Basic Concept": "Error generating concepts"},
                example_questions=[{"question": "Error generating questions", "answer": "N/A", "difficulty": "beginner"}],
                practice_exercises=[{
                    "title": "Basic Exercise",
                    "problem": "Error generating exercises",
                    "solution": "N/A",
                    "difficulty": "beginner"
                }],
                case_studies=[{
                    "title": "Sample Case",
                    "scenario": "Error generating case studies",
                    "challenge": "N/A",
                    "solution": "N/A",
                    "outcome": "N/A",
                    "lessons_learned": ["N/A"],
                    "related_concepts": ["N/A"]
                }]
            )