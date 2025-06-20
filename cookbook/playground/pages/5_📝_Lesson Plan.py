import streamlit as st
from pydantic import BaseModel, Field
from typing import List, Optional
from fpdf import FPDF
from utils.models import client_model
client = client_model()

# Lesson Plan Model
class LessonPlan(BaseModel):
    topic: str
    objectives: List[str]
    introduction: str
    content: str
    assessment: str
    conclusion: str

    def show(self):
        st.markdown(f"### 📘 Lesson Plan for **{self.topic}**")
        st.markdown("#### 🎯 Objectives")
        for obj in self.objectives:
            st.markdown(f"- {obj}")
        st.markdown("#### 🧠 Introduction")
        st.markdown(self.introduction)
        st.markdown("#### 📚 Content")
        st.markdown(self.content)
        st.markdown("#### 📝 Assessment")
        st.markdown(self.assessment)
        st.markdown("#### 🏁 Conclusion")
        st.markdown(self.conclusion)

    def to_pdf(self, path="lesson_plan.pdf", watermark: bool = False):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, f"Lesson Plan - {self.topic}")
        pdf.multi_cell(0, 10, "\nObjectives:")
        for obj in self.objectives:
            pdf.multi_cell(0, 10, f"- {obj}")
        pdf.multi_cell(0, 10, f"\nIntroduction:\n{self.introduction}")
        pdf.multi_cell(0, 10, f"\nContent:\n{self.content}")
        pdf.multi_cell(0, 10, f"\nAssessment:\n{self.assessment}")
        pdf.multi_cell(0, 10, f"\nConclusion:\n{self.conclusion}")

        if watermark:
            pdf.set_text_color(150, 150, 150)
            pdf.set_xy(60, 270)
            pdf.set_font("Arial", size=10, style="I")
            pdf.cell(0, 10, "Educhain · AI-Powered Learning", align="C")

        pdf.output(path)
        return path

# Title and Instructions
st.markdown("<h1 style='text-align: center; color: #6A5ACD;'> 📘 AI-Powered Lesson Plan Generator </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate smart, quality questions instantly using Gemini Flash + EduChain ⚡</p>", unsafe_allow_html=True)
st.markdown("""
Easily create structured lesson plans using AI. Just provide a topic, and we'll take care of the rest — objectives, content, assessments, and even a downloadable PDF!
""")

# Input Section
lesson_topic = st.text_input("Enter a Topic for the Lesson Plan")
add_watermark = st.checkbox("Add Educhain Watermark to PDF", value=True)

# Generate Button
if st.button("📖 Generate Lesson Plan") and lesson_topic:
    with st.spinner("Creating your lesson plan with EduChain magic..."):
        response = client.content_engine.generate_lesson_plan(
            topic=lesson_topic,
            response_model=LessonPlan
        )
        response.show()

        pdf_path = response.to_pdf(watermark=add_watermark)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download Lesson Plan as PDF", f, file_name="lesson_plan.pdf", mime="application/pdf")

st.markdown("---")
st.caption("Powered by EduChain · Gemini Flash 🌟")

with st.popover("Open popover"):
    st.markdown(" Turn On Developer Mode? ")
    Developer_Mode = st.checkbox("Check 'On' to Turn-on Developer Mode")
    
if Developer_Mode == True:
    st.write("Welcome Developers!! Here is an in-depth explanation of all of the tools used here.")
    st.page_link("https://github.com/satvik314/educhain/blob/main/cookbook/features/educhain_generate_lesson_plan.ipynb", label="GitHub", icon = "🔗")
    st.markdown("""
🧠 Overview:
-------------
This Streamlit app allows educators to **automatically generate full lesson plans** using a single topic input. It utilizes EduChain’s content engine with Gemini Flash for generating structured educational plans including:

- Objectives
- Introduction
- Main content
- Assessment ideas
- Conclusion

You can also **download the plan as a PDF**, optionally branded with a watermark.

📦 Setup and Configuration:
-----------------------------
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI

# Load the Gemini API key
GOOGLE_API_KEY = os.getenv("GEMINI_KEY")

# Configure Gemini Flash and Educhain
gemini_flash = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)
flash_config = LLMConfig(custom_model=gemini_flash)
client = Educhain(flash_config)

📐 LessonPlan Model:
----------------------
This app defines a Pydantic model `LessonPlan` that represents the expected structure of the lesson plan returned by Educhain’s API.

It includes fields for:
- topic
- objectives (list of strings)
- introduction
- content
- assessment
- conclusion

Two custom methods:
- `.show()` → Renders the plan in the Streamlit UI.
- `.to_pdf(path, watermark)` → Exports the plan to a downloadable PDF.

🚀 Main Logic:
----------------
When the user inputs a lesson topic and clicks the generate button, the following happens:

1. The topic is sent to:
```python
client.content_engine.generate_lesson_plan(
    topic=lesson_topic,
    response_model=LessonPlan
)
"""
)
