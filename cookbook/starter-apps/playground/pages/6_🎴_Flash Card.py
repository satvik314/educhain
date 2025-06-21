import streamlit as st
from utils.models import client_model
client = client_model()

st.set_page_config(page_title="🧠 Flashcard Generator", layout="wide")
st.markdown("<h1 style='text-align: center; color: #6A5ACD;'>🃏 AI Flashcard Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate clean, effective flashcards instantly using Gemini Flash + EduChain ⚡</p>", unsafe_allow_html=True)
st.divider()

st.subheader("📋 Topic for Flashcards")

with st.form(key="flashcard_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("🔍 Enter Topic", placeholder="e.g., Python Basics")
    with col2:
        num_flashcards = st.slider("🃏 No. of Flashcards", min_value=1, max_value=20, value=5)

    submit = st.form_submit_button("🚀 Generate Flashcards")

if submit and topic:
    with st.spinner("Generating Flashcards using Gemini Flash..."):
        try:
            flashcards = client.content_engine.generate_flashcards(
                topic=topic,
                num=num_flashcards
            )

            st.success("✅ Flashcards Generated Successfully!")
            st.markdown("---")
            for i, card in enumerate(flashcards.flashcards, start=1):
                st.markdown(f"### 🃏 Card {i}")
                st.markdown(f"**Q:** {card.front}")
                st.markdown(f"**A:** {card.back}")
                st.markdown("---")

        except Exception as e:
            st.error(f"❌ Error generating flashcards:\n\n{e}")

st.caption("Crafted with ❤️ by EduChain + Gemini Flash ✨")

with st.popover("Open popover"):
    st.markdown("Turn On Developer Mode?")
    Developer_Mode = st.checkbox("Check 'On' to Turn-on Developer Mode")

if Developer_Mode:
    st.write("Welcome Developers!! Here is an in-depth explanation of all of the tools used here.")
    st.page_link("https://github.com/satvik314/educhain/blob/main/cookbook/features/generate_flashcards_with_educhain.ipynb", label="GitHub", icon="🔗")
    st.markdown("""
📦 Key Initialization
-----------------------------------
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI

# Step 1: Setup the Gemini Flash LLM
gemini_flash = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY
)

# Step 2: Wrap the model in LLMConfig
flash_config = LLMConfig(custom_model=gemini_flash)

# Step 3: Create Educhain client using the model config
client = Educhain(flash_config)

🧠 What Does client.content_engine.generate_flashcards() Do?
--------------------------------------------------------------
This is the core function responsible for generating flashcards from a given topic.

Example:
flashcards = client.content_engine.generate_flashcards(
    topic="Python Basics",
    num=5
)

🔍 It likely does the following:
- Crafts a structured flashcard generation prompt
- Sends it to Gemini Flash
- Parses and returns clean Q&A flashcards

✅ Sample Output:
[
    {
        front: "What is a variable in Python?",
        back: "A storage location for data with a name."
    },
    ...
]

❤️ Summary
Educhain makes flashcard generation effortless using LLMs.
It's perfect for revision, study sessions, and spaced repetition.
    """)