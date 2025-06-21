import streamlit as st
from utils.models import client_model
from PyPDF2 import PdfReader
client = client_model()

st.markdown("<h1 style='text-align: center; color: #6A5ACD;'>📄 Text / PDF / URL to Question Bank </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate smart, quality questions instantly using Gemini Flash + EduChain ⚡</p>", unsafe_allow_html=True)
st.markdown("""
Easily create questions from a block of text, an online article, or an academic PDF.
Select your data source below and customize the question type and difficulty.
""")
st.divider()

source_type = st.selectbox("Choose Source Type", ["Text", "URL", "PDF"], index=0)
num = st.slider("Number of Questions", 1, 20, 5)
question_type = st.selectbox("Question Type", ["Multiple Choice", "True/False", "Fill in the Blank", "Short Answer"])
difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
custom_instr = st.text_area("Custom Instructions (Optional)", "", height=50)

def show_result(result):
    st.success("✅ Questions Generated!")
    for i, q in enumerate(result.questions, 1):
        st.markdown(f"### Q{i}. {q.question}")
        if hasattr(q, "options") and q.options:
            for j, opt in enumerate(q.options):
                st.markdown(f"- **{chr(65+j)}.** {opt}")
            st.markdown(f"✅ **Answer:** `{q.answer}`")
        elif hasattr(q, "answer"):
            st.markdown(f"✅ **Answer:** `{q.answer}`")
            if hasattr(q, "blank_word") and q.blank_word:
                st.caption(f"✏️ Fill in: `{q.blank_word}`")
        if getattr(q, "explanation", None):
            st.info(f"💡 {q.explanation}")
        st.markdown("---")

if source_type == "Text":
    text_input = st.text_area("Paste your content here:", height=200)
    if st.button("🚀 Generate from Text") and text_input:
        with st.spinner("Generating questions from text..."):
            result = client.qna_engine.generate_questions_from_data(
                source=text_input,
                source_type="text",
                num=num,
                question_type=question_type,
                custom_instructions=custom_instr
            )
            show_result(result)

elif source_type == "URL":
    url_input = st.text_input("Enter the URL of an article or webpage:")
    if st.button("🌐 Generate from URL") and url_input:
        with st.spinner("Fetching and processing URL..."):
            result = client.qna_engine.generate_questions_from_data(
                source=url_input,
                source_type="url",
                num=num,
                question_type=question_type,
                difficulty_level=difficulty,
                custom_instructions=custom_instr
            )
            show_result(result)

elif source_type == "PDF":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file and st.button("📄 Generate from PDF"):
        with st.spinner("Extracting text and generating questions..."):
            reader = PdfReader(uploaded_file)
            pdf_text = " ".join([page.extract_text() or "" for page in reader.pages])
            pdf_text = " ".join(pdf_text.split()) 

            result = client.qna_engine.generate_questions_from_data(
                source=pdf_text,
                source_type="text",
                num=num,
                question_type=question_type,
                custom_instructions=custom_instr
            )
            show_result(result)

st.markdown("---")
st.caption("Built with ❤️ using EduChain · Gemini Flash ✨")

with st.popover("Open popover"):
    st.markdown(" Turn On Developer Mode? ")
    Developer_Mode = st.checkbox("Check 'On' to Turn-on Developer Mode")
    
if Developer_Mode == True:
    st.write("Welcome Developers!! Here is an in-depth explanation of all of the tools used here.")
    st.page_link("https://github.com/satvik314/educhain/blob/main/cookbook/features/Bulk_Question_Generation_Using_Educhain.ipynb", label="GitHub", icon = "🔗")
    st.markdown("""
🔧 Overview:
------------
This app lets users generate intelligent, structured questions from three types of data sources:
1. Raw Text
2. Web URL (articles, blogs, etc.)
3. Uploaded PDF documents

It uses the Educhain library with Gemini Flash (via LangChain) to extract and convert content into question banks.

💡 Initialization and Setup:
-----------------------------
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI

# Load Gemini API key from .env
GOOGLE_API_KEY = os.getenv("GEMINI_KEY")

# Create Gemini Flash model and config
gemini_flash = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)
flash_config = LLMConfig(custom_model=gemini_flash)

# Initialize Educhain client
client = Educhain(flash_config)

📥 User Input:
--------------
- Source type: Choose between Text / URL / PDF
- Number of questions
- Question type: MCQ / T/F / Fill-in / Short Answer
- Difficulty: Beginner / Intermediate / Advanced
- Optional: Custom instructions to guide the model (e.g., “focus on factual questions”)

🔍 How Generation Works:
--------------------------
For each data type, the app calls:

client.qna_engine.generate_questions_from_data(
    source=...,                # raw text, URL, or filepath
    source_type="text|url|pdf",
    num=...,                   # number of questions
    question_type=...,         # question format
    difficulty_level=...,      # difficulty
    custom_instructions=...    # optional text
)

Educhain handles:
- Reading and preprocessing the source (e.g., parsing PDF or scraping URL)
- Prompting Gemini Flash with structured prompts
- Extracting Q&A from the response

📤 Streamlit Display:
----------------------
A helper function `show_result()` displays the generated questions:
- Numbered question titles
- Answer options (for MCQ)
- Final answer (highlighted)
- Explanation or fill-in-the-blank word, if present

Example output display:

### Q1. What is photosynthesis?
- A. Energy from the moon
- B. Conversion of light to chemical energy
✅ Answer: B
💡 Explanation: Photosynthesis is the conversion of light energy into chemical energy by plants.

📁 Special Notes on PDF Handling:
-----------------------------------
- Uploaded PDF is saved temporarily as `temp_uploaded.pdf`
- This file path is passed to Educhain which extracts the text from the document internally before generating questions

❤️ Summary:
-------------
This Streamlit app provides a seamless way to generate question banks from multiple content formats. The combination of:
- LangChain + Gemini Flash for fast LLM response
- Educhain for educational logic
- Streamlit for clean UI

...makes it a powerful tool for teachers, students, and edtech developers alike.
""")
