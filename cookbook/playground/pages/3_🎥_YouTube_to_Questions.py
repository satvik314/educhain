import streamlit as st
from utils.models import client_model
client = client_model()

# Title and instructions
st.markdown("<h1 style='text-align: center; color: #6A5ACD;'>🎥 YouTube to Questions </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate smart, quality questions instantly using Gemini Flash + EduChain ⚡</p>", unsafe_allow_html=True)
st.markdown("""
Paste a YouTube video URL and generate questions from the content!
Make sure the video has subtitles or clear speech for best results.
""")

# Input controls
video_url = st.text_input("Enter YouTube Video URL")
num_questions = st.slider("Number of Questions", 1, 20, 5)
question_type = st.selectbox("Question Type", ["Multiple Choice", "True/False", "Fill in the Blank", "Short Answer"])
difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
custom_instr = st.text_area("Custom Instructions (Optional)", "", height=50)

# Function to display results
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

# Button action
if st.button("🚀 Generate from YouTube") and video_url:
    with st.spinner("Processing video and generating questions..."):
        result = client.qna_engine.generate_questions_from_youtube(
            url=video_url,
            num=num_questions,
            question_type=question_type,
            difficulty_level=difficulty,
            custom_instructions=custom_instr
        )
        show_result(result)

st.markdown("---")
st.caption("Powered by EduChain QnA Engine · Gemini Flash ✨")

with st.popover("Open popover"):
    st.markdown(" Turn On Developer Mode? ")
    Developer_Mode = st.checkbox("Check 'On' to Turn-on Developer Mode")
    
if Developer_Mode == True:
    st.write("Welcome Developers!! Here is an in-depth explanation of all of the tools used here.")
    st.page_link("https://github.com/satvik314/educhain/blob/main/cookbook/features/Generate_questions_from_youtube.ipynb", label="GitHub", icon = "🔗")
    st.markdown("""
🔧 Overview:
------------
This Streamlit app allows users to input a YouTube video link and automatically generate structured questions from its content using Gemini Flash via Educhain.

It is ideal for turning educational videos, lectures, or tutorials into practice material — assuming the video has subtitles or clear speech.

📦 Initialization and Setup:
-----------------------------
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI

# Load Gemini API key from .env
GOOGLE_API_KEY = os.getenv("GEMINI_KEY")

# Create Gemini Flash model and wrap it
gemini_flash = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY
)

# Configure and initialize Educhain
flash_config = LLMConfig(custom_model=gemini_flash)
client = Educhain(flash_config)

📝 User Inputs:
----------------
- YouTube Video URL
- Number of questions to generate
- Question type (MCQ, True/False, Fill in the Blank, Short Answer)
- Difficulty level (Beginner, Intermediate, Advanced)
- Optional instructions for tone/style/focus

🚀 Main Function:
------------------
The core function triggered on clicking the button:

client.qna_engine.generate_questions_from_youtube(
    url=video_url,
    num=num_questions,
    question_type=question_type,
    difficulty_level=difficulty,
    custom_instructions=custom_instr
)

✨ Internally, this likely performs:
- Downloading/transcribing audio or extracting captions from the YouTube video
- Summarizing or chunking the video content
- Prompting Gemini Flash with structured instructions
- Parsing the response to generate clear, formatted Q&A objects

📤 Display Logic:
------------------
Results are rendered using the `show_result()` function:
- Displays each question in numbered format
- Lists options for MCQs with the correct answer
- Shows answer directly for other types
- Explanation is shown in an info box if available
- Fill-in-the-blank word is displayed for that type

Example:

### Q1. What is the boiling point of water?
- A. 50°C
- B. 100°C
- C. 150°C
✅ Answer: B
💡 Explanation: Water boils at 100°C under standard pressure.

🧠 Benefits:
------------
- Great for educators converting lectures to quizzes
- Students can auto-generate practice material from videos
- Supports multiple formats and difficulty tuning

⚠️ Tip:
--------
- Videos must have clear speech or captions for best accuracy.
- For noisy, silent, or music-based videos, question quality may drop.

❤️ Summary:
-------------
This YouTube-powered question generation app uses:
- Gemini Flash for fast LLM responses
- Educhain to handle transcription, prompting, and parsing
- Streamlit for a clean user interface

Together, they provide a powerful way to generate assessments from video learning content.
""")