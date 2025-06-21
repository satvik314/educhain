import streamlit as st
from utils.models import client_model
client = client_model()

st.set_page_config(page_title="🧠 Generate Questions", layout="wide")
st.markdown("<h1 style='text-align: center; color: #6A5ACD;'>🧠 AI-Powered Question Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate smart, quality questions instantly using Gemini Flash + EduChain ⚡</p>", unsafe_allow_html=True)
st.divider()
st.subheader("📋 Topic & Options")

with st.form(key="question_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("🔍 Enter Topic", placeholder="e.g., Thermodynamics")
    with col2:
        num_questions = st.slider("📊 No. of Questions", min_value=1, max_value=20, value=5)

    qtype = st.selectbox("❓ Question Type", [
        "Multiple Choice",
        "True/False",
        "Fill in the Blank",
        "Short Answer"
    ])
    instructions = st.text_area("📝 Custom Instructions (Optional)", placeholder="e.g., Focus on beginner-level concepts")

    submit = st.form_submit_button("🚀 Generate Questions")

if submit and topic:
    with st.spinner("Thinking with Gemini Flash..."):
        try:
            result = client.qna_engine.generate_questions(
                topic=topic,
                num=num_questions,
                question_type=qtype,
                custom_instructions=instructions
            )

            st.success("✅ Questions Generated Successfully!")
            st.markdown("---")
            for i, q in enumerate(result.questions, start=1):
                st.markdown(f"### Q{i}. {q.question}")
                if hasattr(q, "options") and q.options:
                    for j, opt in enumerate(q.options):
                        st.markdown(f"- **{chr(65+j)}.** {opt}")
                    st.markdown(f"✅ **Correct Answer:** `{q.answer}`")
                elif hasattr(q, "answer"):
                    st.markdown(f"✅ **Answer:** `{q.answer}`")
                    if hasattr(q, "blank_word") and q.blank_word:
                        st.caption(f"✏️ Fill in: `{q.blank_word}`")
                if getattr(q, "explanation", None):
                    st.info(f"💡 {q.explanation}")
                st.markdown("---")

        except Exception as e:
            st.error(f"❌ Error generating questions:\n\n{e}")

st.caption("Crafted with ❤️ by EduChain + Gemini Flash ✨")


with st.popover("Open popover"):
    st.markdown(" Turn On Developer Mode? ")
    Developer_Mode = st.checkbox("Check 'On' to Turn-on Developer Mode")
    
if Developer_Mode == True:
    st.write("Welcome Developers!! Here is an in-depth explanation of all of the tools used here.")
    st.page_link("https://github.com/satvik314/educhain/blob/main/cookbook/features/Generate_MCQs_from_Data_Educhain_v3.ipynb", label="GitHub", icon = "🔗")
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

🧠 What Does client.qna_engine.generate_questions() Do?
----------------------------------------------------------
This is the core function responsible for generating questions from a given topic.

Example:
result = client.qna_engine.generate_questions(
    topic=topic,
    num=num_questions,
    question_type=qtype,
    custom_instructions=instructions
)

🔍 It likely does the following:
- Builds a prompt using topic, number, type, and instructions
- Calls the Gemini Flash model with the prompt
- Parses and returns a structured list of question objects

✅ Sample Output:
[
    {
        question: "What is the first law of thermodynamics?",
        options: ["Energy cannot be created", "Energy can be destroyed", ...],
        answer: "A",
        explanation: "The first law states...",
        blank_word: "energy"  # For fill-in-the-blank type
    },
    ...
]

🧪 What are Custom Instructions?
------------------------------------
This is an optional input that enhances control over output. Examples:
- "Beginner level"
- "Only fact-based MCQs"
- "Include short explanations"
These get incorporated in the prompt to guide the LLM better.

🖼️ Output Rendering in Streamlit
-------------------------------------
After generation, each question is displayed:
- With options (for MCQ)
- Answer is shown clearly
- Explanation is highlighted
- Fill-in-the-blank terms are captioned

❤️ Summary
Educhain simplifies interaction with LLMs like Gemini Flash by:
- Abstracting prompt engineering
- Managing model interaction
- Parsing the result into clean Q&A format

It gives you a plug-and-play question generation engine, perfect for educational tools.
""")
