import streamlit as st
from pathlib import Path

st.set_page_config(page_title="EduChain Dashboard", layout="wide")
st.image("https://raw.githubusercontent.com/Shubhwithai/GRE_Geometry_quiz/refs/heads/main/Group%2042.png")
st.markdown("<h4 style='text-align: center;'> AI-Powered Educational Platform. </h4>", unsafe_allow_html=True)

st.page_link("https://github.com/satvik314/educhain", label="GitHub", icon = "🔗")
st.page_link("https://educhain.in/", label = "Educhain", icon = "🌍")

st.markdown("<h1 style='text-align: center; color: White;'> Welcome to the Educhain PlayGround </h1>", unsafe_allow_html=True)

# Optional quick stats or intro dashboard
tabs = st.tabs(["✨ Feature Highlights", "🧑‍💻Developer Hub"])
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8, gap = "large")

with tabs[0]:
    with col1:
        st.image("https://raw.githubusercontent.com/Shubhwithai/GRE_Geometry_quiz/refs/heads/main/Group%2042.png", width = 100)
        st.page_link("Home.py", label="Home", icon="🏠")
    with col2:
        st.image("https://ik.imagekit.io/o0nppkxow/file_0000000099c461f58aedf4df5233f24f.png?updatedAt=1750366839854", width = 100)
        st.page_link("pages/1_🧠_Generate_Questions.py", label="Ques Generator", icon="1️⃣")
    with col3:
        st.image("https://ik.imagekit.io/o0nppkxow/file_0000000071e061fa800b5282b25dd1a9.png?updatedAt=1750366839719", width = 100)
        st.page_link("pages/2 📄_Generate From Text-PDF-URL.py", label="PDF/URL", icon="2️⃣")
    with col4:
        st.image("https://ik.imagekit.io/o0nppkxow/file_00000000182462309b57be2d9ca44084.png?updatedAt=1750366839798", width = 100)
        st.page_link("pages/3_🎥_YouTube_to_Questions.py", label="YouTube", icon="3️⃣")
    with col5:
        st.image("https://ik.imagekit.io/o0nppkxow/file_00000000ac5461fbb3534dfb9e11aa90.png?updatedAt=1750366872461", width = 100)
        st.page_link("pages/4_🔮_Doubt Solver.py", label="Doubt Solver", icon="4️⃣")
    with col6:
        st.image("https://ik.imagekit.io/o0nppkxow/file_00000000ce38622faa56e5ecd9b2d62c.png?updatedAt=1750366839851", width = 100)
        st.page_link("pages/5_📝_Lesson Plan.py", label="Lesson Plan", icon="5️⃣")
    with col7:
        st.image("https://ik.imagekit.io/o0nppkxow/file_00000000484461f4a82c4a0e5a1ddfb2.png?updatedAt=1750378296389", width = 100)
        st.page_link("pages/6_🎴_Flash Card.py", label="Flash Card", icon="6️⃣")
    with col8:
        st.image("https://ik.imagekit.io/o0nppkxow/file_000000002de461f8a5e4a7ea89406f3d.png?updatedAt=1750378296410", width = 100)
        st.page_link("pages/7_PYQ to Pre Tool.py", label="PYQ to Prep", icon="7️⃣")

with tabs[1]:
    with st.expander("## 📝 Generate Multiple Choice Questions (MCQs) "):
        st.markdown("""
````python
from educhain import Educhain

client = Educhain()

# Basic MCQ generation
mcq = client.qna_engine.generate_questions(
    topic="Solar System",
    num=3,
    question_type="Multiple Choice"
)

# Advanced MCQ with custom parameters
advanced_mcq = client.qna_engine.generate_questions(
    topic="Solar System",
    num=3,
    question_type="Multiple Choice",
    difficulty_level="Hard",
    custom_instructions="Include recent discoveries"
)

print(mcq.model_dump_json())  # View in JSON format , For Dictionary format use mcq.model_dump()
````
""")
    with st.expander("## 📊 Create Lesson Plans "):
        st.markdown("""
````python
from educhain import Educhain

client = Educhain()

# Basic lesson plan
lesson = client.content_engine.generate_lesson_plan(
    topic="Photosynthesis"
)

# Advanced lesson plan with specific parameters
detailed_lesson = client.content_engine.generate_lesson_plan(
    topic="Photosynthesis",
    duration="60 minutes",
    grade_level="High School",
    learning_objectives=["Understanding the process", "Identifying key components"]
)

print(lesson.model_dump_json())  # View in JSON format , For Dictionary format use lesson.model_dump()
````
""")
    with st.expander("## 🔄 Support for Various LLM Models "):
        st.page_link("https://github.com/satvik314/educhain/tree/main/cookbook/providers", label="GitHub", icon = "🔗")
        st.markdown("""
````python
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Using Gemini
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key="YOUR_GOOGLE_API_KEY"
)
gemini_config = LLMConfig(custom_model=gemini_model)
gemini_client = Educhain(gemini_config)

# Using GPT-4
gpt4_model = ChatOpenAI(
    model_name="gpt-4.1",
    openai_api_key="YOUR_OPENAI_API_KEY"
)
gpt4_config = LLMConfig(custom_model=gpt4_model)
gpt4_client = Educhain(gpt4_config)
````
""")
    with st.expander("## 📁 Export Questions to Different Formats "):
        st.markdown("""
````python
from educhain import Educhain

client = Educhain()
questions = client.qna_engine.generate_questions(topic="Climate Change", num=5)

# Export to JSON
questions.json("climate_questions.json")

# Export to PDF
questions.to_pdf("climate_questions.pdf")

# Export to CSV
questions.to_csv("climate_questions.csv")
````
""")
    with st.expander("## 🎨 Customizable Prompt Templates"):
        st.markdown("""
````python
from educhain import Educhain

client = Educhain()

# Custom template for questions
custom_template = '''
Generate {num} {question_type} questions about {topic}.
Ensure the questions are:
- At {difficulty_level} level
- Focus on {learning_objective}
- Include practical examples
- {custom_instructions}
'''

questions = client.qna_engine.generate_questions(
    topic="Machine Learning",
    num=3,
    question_type="Multiple Choice",
    difficulty_level="Intermediate",
    learning_objective="Understanding Neural Networks",
    custom_instructions="Include recent developments",
    prompt_template=custom_template
)
````
""")
    with st.expander("## 📚 Generate Questions from Files"):
        st.markdown("""
````python
from educhain import Educhain

client = Educhain()

# From URL
url_questions = client.qna_engine.generate_questions_from_data(
    source="https://example.com/article",
    source_type="url",
    num=3
)

# From PDF
pdf_questions = client.qna_engine.generate_questions_from_data(
    source="path/to/document.pdf",
    source_type="pdf",
    num=3
)

# From Text File
text_questions = client.qna_engine.generate_questions_from_data(
    source="path/to/content.txt",
    source_type="text",
    num=3
)
````
""")
    with st.expander("## 📹 Generate Questions from YouTube Videos"):
        st.markdown("""
````python
from educhain import Educhain

client = Educhain()

# Basic usage - Generate 3 MCQs from a YouTube video
questions = client.qna_engine.generate_questions_from_youtube(
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    num=3
)
print(questions.model_dump_json())

# Generate questions preserving original language
preserved_questions = client.qna_engine.generate_questions_from_youtube(
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    num=2,
    target_language='hi',
    preserve_original_language=True  # Keeps original language
)
""")
    with st.expander("## 🥽 Generate Questions from Images"):
        st.markdown("""
````python
from educhain import Educhain

client = Educhain() #Default is 4o-mini (make sure to use a multimodal LLM!)

question = client.qna_engine.solve_doubt(
    image_source="path-to-your-image",
    prompt="Explain the diagram in detail",
    detail_level = "High" 
    )

print(question)
````
""")
    with st.expander("## 🥽 Generate Visual Questions"):
        st.markdown("""
````python
from langchain_google_genai import ChatGoogleGenerativeAI
from educhain import Educhain, LLMConfig

gemini_flash = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

flash_config = LLMConfig(custom_model=gemini_flash)

client = Educhain(flash_config)

ques = client.qna_engine.generate_visual_questions(
        topic="GMAT Statistics", num=10 )

print(ques.model_dump_json())
````
""")

st.markdown("---")
st.caption("Built by EduChain Innovators — 2025 🛠️")
