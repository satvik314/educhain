from typing import Optional, Type, Any
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from educhain.core.config import LLMConfig
from educhain.models.content_models import LessonPlan

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