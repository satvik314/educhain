import streamlit as st
from pydantic import BaseModel, Field
from typing import List, Optional

from utils.models import client_model
client = client_model()

class SolvedDoubt(BaseModel):
    explanation: str
    steps: Optional[List[str]] = Field(default_factory=list)
    additional_notes: Optional[str] = None

st.markdown("<h1 style='text-align: center; color: #6A5ACD;'> 🔮 Visual Doubt Solver </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Generate smart, quality questions instantly using Gemini Flash + EduChain ⚡</p>", unsafe_allow_html=True)
st.markdown("""
Upload a question image or diagram and receive a detailed step-by-step explanation.
You can optionally add a specific prompt to guide the response.
""")

image_file = st.file_uploader("Upload Image of the Doubt (JPG/PNG)", type=["jpg", "jpeg", "png"])
prompt_text = st.text_area("Add a Custom Prompt (Optional)", "Explain this image in detail.")
detail_level = st.selectbox("Explanation Detail Level", ["High", "Medium", "Low"], index=0)

def show_doubt_solution(result: SolvedDoubt):
    st.success("✅ Doubt Solved!")

    st.markdown("### 📄 Explanation")
    st.markdown(result.explanation)

    if result.steps:
        st.markdown("### 🔹 Steps:")
        for i, step in enumerate(result.steps, 1):
            st.markdown(f"**{i}.** {step}")

    if result.additional_notes:
        st.markdown("### 📄 Additional Notes")
        st.markdown(result.additional_notes)

if st.button("🚀 Solve Doubt") and image_file:
    with st.spinner("Solving your visual doubt with AI..."):
        img_path = "temp_doubt_image.png"
        with open(img_path, "wb") as f:
            f.write(image_file.read())

        raw_result = client.qna_engine.solve_doubt(
            image_source=img_path,
            prompt=prompt_text,
            detail_level=detail_level
        )
        parsed_result = raw_result  
        show_doubt_solution(parsed_result)


st.markdown("---")
st.caption("Powered by EduChain Doubt Solver · Gemini Flash 🌟")

with st.popover("Open popover"):
    st.markdown(" Turn On Developer Mode? ")
    Developer_Mode = st.checkbox("Check 'On' to Turn-on Developer Mode")
    
if Developer_Mode == True:
    st.write("Welcome Developers!! Here is an in-depth explanation of all of the tools used here.")
    st.markdown(""" Code Use:
from educhain import Educhain

client = Educhain() #Default is 4o-mini (make sure to use a multimodal LLM!)

question = client.qna_engine.solve_doubt(
    image_source="https://i.ytimg.com/vi/OQjkFQAIOck/maxresdefault.jpg",
    prompt="Explain the diagram in detail",
    detail_level = "High"
    )

print(question)
""")
    st.markdown("""
📷 Overview:
-------------
This Streamlit app allows users to upload an image (question diagram, handwritten math problem, etc.) and receive an AI-generated detailed explanation. 
It uses the Educhain `solve_doubt()` engine powered by Gemini Flash to interpret and respond intelligently to visual content.

📦 Initialization and Setup:
-----------------------------
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API key
GOOGLE_API_KEY = os.getenv("GEMINI_KEY")

# Create Gemini Flash wrapper and config
gemini_flash = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY
)

# Setup Educhain client
flash_config = LLMConfig(custom_model=gemini_flash)
client = Educhain(flash_config)

🧠 Model Definition:
---------------------
Using Pydantic for structured parsing of Educhain's `SolvedDoubt` output:

class SolvedDoubt(BaseModel):
    explanation: str
    steps: Optional[List[str]] = Field(default_factory=list)
    additional_notes: Optional[str] = None

This ensures the response from the AI is structured and easily renderable in Streamlit.

📝 User Inputs:
----------------
- Image upload: PNG, JPG, or JPEG
- Custom prompt: Optional input to guide explanation (e.g., "Explain this in the context of algebra")
- Detail level: High / Medium / Low, influencing how comprehensive the answer will be

🚀 Main Function Call:
-----------------------
Upon clicking “Solve Doubt”, the app:

1. Saves the uploaded image temporarily.
2. Calls:
   client.qna_engine.solve_doubt(
       image_source=img_path,
       prompt=prompt_text,
       detail_level=detail_level
   )

This triggers:
- Image understanding (possibly OCR or visual LLM parsing)
- Prompt fusion (merging the image with your optional instruction)
- LLM-based reasoning and response generation

📤 Output Rendering:
----------------------
The AI-generated explanation is shown in sections:

- 📄 Explanation: Main concept or answer derived from the image
- 🔹 Steps: If present, a breakdown of logical/mathematical steps
- 📄 Additional Notes: Extra insights, tips, or warnings (optional)

Example:

📄 Explanation:
"This is a graph of a quadratic function with roots at x = 1 and x = 3..."

🔹 Steps:
1. Identify the function structure.
2. Note key points and curvature.
3. Solve for x-intercepts using the factorized form.

📄 Additional Notes:
"The vertex lies at the midpoint of the roots: x = 2."

🧠 Benefits:
-------------
- Converts visual academic content into detailed understanding
- Great for solving diagrams, geometry, physics questions, etc.
- Helps students get clarity without typing the entire question

❤️ Summary:
-------------
The Visual Doubt Solver is powered by:
- EduChain’s visual QnA engine
- Gemini Flash for fast, rich language understanding
- Streamlit for interactive UX

It creates a seamless experience to turn images into structured, step-by-step learning.
"""
)
