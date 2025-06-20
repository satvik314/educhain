import streamlit as st
from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from typing import List, Type, Any
import os
from typing import Optional, Any

class LLMConfig:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gpt-4o-mini",
        max_tokens: int = 1500,
        temperature: float = 0.7,
        custom_model: Optional[Any] = None,
        base_url: Optional[str] = None,
        default_headers: Optional[dict] = None
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.custom_model = custom_model
        self.base_url = base_url
        self.default_headers = default_headers

class Flashcard(BaseModel):
    front: str = Field(..., description="The front side of the flashcard with a question or key term")
    back: str = Field(..., description="The back side of the flashcard with the answer or definition")
    explanation: Optional[str] = Field(None, description="An optional explanation or additional context")
    card_type: Optional[str] = Field("Concept", description="The type of flashcard (e.g., Concept, Definition, Fact, Process)")

class FlashcardSet(BaseModel):
    title: str = Field(..., description="The title or topic of the flashcard set")
    flashcards: List[Flashcard] = Field(..., description="A list of flashcards in this set")
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
            4. A card type that categorizes the flashcard (choose from: Concept, Definition, Fact, Process, Example, Comparison)

            The flashcards should cover key concepts, terminology, and important facts related to the topic.
            Mix different card types to create a comprehensive learning experience.

            Ensure that the output follows this structure:
            - A title for the flashcard set (the main topic)
            - A list of flashcards, each containing:
              - front: The question or key term
              - back: The answer or definition
              - explanation: Additional context or explanation (optional)
              - card_type: The type of flashcard (e.g., Concept, Definition, Fact, Process, Example, Comparison)
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

st.set_page_config(page_title="EduChain Flashcard Generator", page_icon="📚")

st.title("📚 educhain Flashcard Generator")

# Add a brief description
st.markdown("""
Generate custom flashcards on any topic using AI! Perfect for studying and quick learning.
""")

# API Key section
st.sidebar.header("🔑 API Key Settings")
api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key:",
    type="password",
    help="Your API key will not be stored and is only used for this session."
)

if api_key:
    st.sidebar.success("✅ API Key provided")
else:
    st.sidebar.warning("⚠️ Please enter your OpenAI API key to continue")

# Initialize ContentEngine with the appropriate API key
if api_key:
    llm_config = LLMConfig(api_key=api_key)
    content_engine = ContentEngine(llm_config)

# User input with improved styling
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input("📝 Enter the topic for flashcards:", placeholder="e.g., Python Programming")
with col2:
    num_cards = st.number_input("🔢 Number of cards:", min_value=1, max_value=20, value=5)

generate_button = st.button("🚀 Generate Flashcards")

if generate_button:
    if not api_key:
        st.error("❌ No API key available. Please provide an API key to continue.")
    elif topic:
        with st.spinner("🧠 Generating flashcards..."):
            flashcard_set = content_engine.generate_flashcards(topic, num=num_cards)
        
        st.success(f"✅ Generated {len(flashcard_set.flashcards)} flashcards for '{flashcard_set.title}'")
        
        # Display flashcards with improved styling
        for i, flashcard in enumerate(flashcard_set.flashcards, 1):
            # Get card type with fallback to "Concept" if not specified
            card_type = getattr(flashcard, 'card_type', "Concept")
            
            # Create a color based on card type
            type_colors = {
                "Concept": "#FF6B6B",  # Red
                "Definition": "#4ECDC4",  # Teal
                "Fact": "#FFD166",  # Yellow
                "Process": "#6A0572",  # Purple
                "Example": "#1A936F",  # Green
                "Comparison": "#3D5A80"  # Blue
            }
            type_color = type_colors.get(card_type, "#888888")
            
            # Create the card header (without HTML, which will be added separately)
            card_header = f"Flashcard {i}: {flashcard.front}"
            
            # Create the expander without HTML
            with st.expander(card_header):
                # Add the type badge separately using markdown with HTML
                st.markdown(f"<span style='float:right; background-color:{type_color}; color:white; padding:2px 8px; border-radius:10px; font-size:0.8em;'>{card_type}</span>", unsafe_allow_html=True)
                st.markdown(f"**Back:** {flashcard.back}")
                if flashcard.explanation:
                    st.markdown(f"**Explanation:** {flashcard.explanation}")
    else:
        st.warning("⚠️ Please enter a topic for the flashcards.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #888;">
        Made with ❤️ by <a href="https://github.com/satvik314/educhain" target="_blank">educhain</a> | Powered by AI
    </div>
    """,
    unsafe_allow_html=True
)

# CSS to style the flashcards and overall app