import streamlit as st
from pydantic import BaseModel, Field
from typing import List, Optional
from fpdf import FPDF
from utils.models import client_model

client = client_model()

class MainTopic(BaseModel):
    title: str
    description: str
    activities: List[str]

class LessonPlan(BaseModel):
    title: str = Field(..., description="The overall title of the lesson plan.")
    subject: str = Field(..., description="The subject area of the lesson.")
    learning_objectives: List[str] = Field(..., description="Learning objectives.")
    lesson_introduction: str = Field(..., description="Introduction to the topic.")
    main_topics: List[MainTopic] = Field(..., description="Topics and activities.")
    learning_adaptations: Optional[str] = None
    real_world_applications: Optional[str] = None
    ethical_considerations: Optional[str] = None

    def show(self):
        st.markdown(f"## 📘 {self.title}")
        st.markdown(f"**Subject:** {self.subject}")

        st.markdown("### 🎯 Learning Objectives")
        for obj in self.learning_objectives:
            st.markdown(f"- {obj}")

        st.markdown("### 🧠 Introduction")
        st.markdown(self.lesson_introduction)

        st.markdown("### 📚 Main Topics")
        for idx, topic in enumerate(self.main_topics, 1):
            st.markdown(f"#### {idx}. {topic.title}")
            st.markdown(topic.description)
            st.markdown("**Activities:**")
            for act in topic.activities:
                st.markdown(f"- {act}")

        if self.learning_adaptations:
            st.markdown("### 🔄 Learning Adaptations")
            st.markdown(self.learning_adaptations)

        if self.real_world_applications:
            st.markdown("### 🌐 Real-World Applications")
            st.markdown(self.real_world_applications)

        if self.ethical_considerations:
            st.markdown("### ⚖️ Ethical Considerations")
            st.markdown(self.ethical_considerations)

    def to_pdf(self, path="lesson_plan.pdf", watermark: bool = False):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_auto_page_break(auto=True, margin=15)

        def write(text):
            pdf.multi_cell(0, 10, text)

        write(f"Lesson Plan - {self.title}")
        write(f"\nSubject: {self.subject}\n")
        write("Objectives:")
        for obj in self.learning_objectives:
            write(f"- {obj}")

        write("\nIntroduction:\n" + self.lesson_introduction)

        for idx, topic in enumerate(self.main_topics, 1):
            write(f"\n{idx}. {topic.title}\n{topic.description}")
            write("Activities:")
            for act in topic.activities:
                write(f"- {act}")

        if self.learning_adaptations:
            write("\nLearning Adaptations:\n" + self.learning_adaptations)

        if self.real_world_applications:
            write("\nReal-World Applications:\n" + self.real_world_applications)

        if self.ethical_considerations:
            write("\nEthical Considerations:\n" + self.ethical_considerations)

        if watermark:
            pdf.set_text_color(150, 150, 150)
            pdf.set_xy(60, 270)
            pdf.set_font("Arial", size=10, style="I")
            pdf.cell(0, 10, "EduChain · AI-Powered Learning", align="C")

        pdf.output(path)
        return path
    
st.markdown("<h1 style='text-align: center; color: #6A5ACD;'>📘 AI-Powered Lesson Plan Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate complete academic lesson plans using Gemini Flash + EduChain ⚡</p>", unsafe_allow_html=True)
lesson_topic = st.text_input("🔎 Enter a Topic for the Lesson Plan")
add_watermark = st.checkbox("Add Educhain Watermark to PDF", value=True)

if st.button("📖 Generate Lesson Plan") and lesson_topic:
    with st.spinner("Generating your lesson plan..."):
        try:
            result = client.content_engine.generate_lesson_plan(
                topic=lesson_topic,
                response_model = LessonPlan
            )
            result.show()

            pdf_path = result.to_pdf(watermark=add_watermark)
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download Lesson Plan as PDF", f, file_name="lesson_plan.pdf", mime="application/pdf")

        except Exception as e:
            st.error("❌ Failed to parse the lesson plan. The topic might be too short or malformed.")
            st.exception(e)

st.markdown("---")
st.caption("Built with ❤️ using EduChain · Gemini Flash 🌟")


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
