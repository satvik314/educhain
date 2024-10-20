from typing import Optional, Type, Any
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from educhain.core.config import LLMConfig
from educhain.models.content_models import LessonPlan
from educhain.models.content_models import FlashcardSet 


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
            Create a comprehensive lesson plan for the following topic:
            Topic: {topic}

            Include the following elements in your lesson plan:
            1. Title of the lesson
            2. Subject area
            3. Main topics (2-3)
            4. For each main topic:
               a. Title
               b. 2-3 subtopics
               c. For each subtopic:
                  - Title
                  - Content elements (definitions, examples, explanations, activities)

            Ensure that the lesson plan is adaptable to different grade levels and teaching contexts.
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\n\nThe response should be in JSON format.\n{format_instructions}"

        lesson_plan_prompt = PromptTemplate(
            input_variables=["topic"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        llm_to_use = llm if llm is not None else self.llm

        lesson_plan_chain = lesson_plan_prompt | llm_to_use
        results = lesson_plan_chain.invoke(
            {"topic": topic, **kwargs},
        )
        results = results.content

        try:
            structured_output = parser.parse(results)
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results)
            return response_model()
    
    def generate_flashcards(
        self,
        topic: str,
        num: int = 10,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        llm: Optional[Any] = None,
        **kwargs
    ) -> FlashcardSet:
        if response_model is None:
            response_model = FlashcardSet
        parser = PydanticOutputParser(pydantic_object=response_model)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            Generate a set of {num} flashcards on the topic: {topic}.

            For each flashcard, provide:
            1. A front side with a question or key term
            2. A back side with the answer or definition
            3. An optional explanation or additional context

            The flashcards should cover key concepts, terminology, and important facts related to the topic.

            Ensure that the output follows this structure:
            - A title for the flashcard set (the main topic)
            - A list of flashcards, each containing:
              - front: The question or key term
              - back: The answer or definition
              - explanation: Additional context or explanation (optional)
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\n\nThe response should be in JSON format.\n{format_instructions}"

        flashcard_prompt = PromptTemplate(
            input_variables=["num", "topic"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        llm_to_use = llm if llm is not None else self.llm
        flashcard_chain = flashcard_prompt | llm_to_use
        results = flashcard_chain.invoke(
            {"num": num, "topic": topic, **kwargs},
        )

        try:
            structured_output = parser.parse(results.content)
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results.content)
            return FlashcardSet(title=topic, flashcards=[])
