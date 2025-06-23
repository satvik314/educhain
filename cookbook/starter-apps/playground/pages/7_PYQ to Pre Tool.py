import streamlit as st
from PyPDF2 import PdfReader
from utils.models import client_model
client = client_model()

st.set_page_config(page_title="📘 PYQ-to-Prep", layout="wide")
st.markdown("<h1 style='text-align: center; color: #6A5ACD;'>📘 PYQ-to-Prep: Smarter Practice from Past Papers</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Upload PYQs or Type Your Own to Auto-Generate Practice Questions with AI ⚡</p>", unsafe_allow_html=True)
st.divider()

st.subheader("🎛️ Select Your Input Mode")
mode = st.radio("Input Method", ["Upload PYQ PDF", "Paste Text Content", "Mock Practice (AI-Generated)"])

def clear_quiz_session_state():
    for key in list(st.session_state.keys()):
        if key.startswith("q") and isinstance(st.session_state[key], str):
            del st.session_state[key]

def display_questions(result):
    st.success("🎯 Smart Questions Ready!")
    score = 0

    for i, q in enumerate(result.questions, 1):
        st.markdown(f"### Q{i}. {q.question}")
        answer_key = f"q{i}"

        if hasattr(q, "options") and q.options:
            selected = st.radio("Choose an answer:", q.options, key=answer_key)
            correct_ans = q.answer
            if selected == correct_ans:
                score += 1
        else:
            st.markdown(f"✅ **Answer:** `{q.answer}`")

        if getattr(q, "explanation", None):
            st.info(f"💡 {q.explanation}")
        st.markdown("---")

    if result.questions:
        st.success(f"Your Score: {score}/{len(result.questions)}")

if mode == "Upload PYQ PDF":
    uploaded_file = st.file_uploader("📄 Upload PYQ PDF File", type=["pdf"])
    doubt = st.text_input("❓ Got Doubt on Specific Portion? Mention It Here (Optional)")
    num_q = st.slider("🔢 Number of Practice Questions", 5, 30, 10)

    if st.button("⚡ Generate from PDF") and uploaded_file:
        with st.spinner("Reading your PYQ and preparing questions..."):
            clear_quiz_session_state()
            reader = PdfReader(uploaded_file)
            text = " ".join([page.extract_text() or "" for page in reader.pages])
            text = " ".join(text.split())

            prompt = doubt if doubt else "Generate diverse questions from this PYQ"
            result = client.qna_engine.generate_questions_from_data(
                source=text,
                source_type="text",
                num=num_q,
                custom_instructions="Generate a mix of MCQs, True/False, Short and Long Answer questions based on this content. Add Bloom's taxonomy & difficulty levels where relevant."
            )
            st.session_state["pdf_result"] = result
            clear_quiz_session_state()

    if "pdf_result" in st.session_state and mode == "Upload PYQ PDF":
        display_questions(st.session_state["pdf_result"])

elif mode == "Paste Text Content":
    user_text = st.text_area("📝 Paste Your PYQ Text Here", height=300)
    doubt = st.text_input("❓ Any Specific Doubt to Focus On? (Optional)")
    num_q = st.slider("🔢 Number of Practice Questions", 5, 30, 10)

    if st.button("📘 Generate from Text") and user_text.strip():
        with st.spinner("Analyzing text and building questions..."):
            clear_quiz_session_state()
            prompt = doubt if doubt else "Create useful questions from this content"
            result = client.qna_engine.generate_questions_from_data(
                source=user_text,
                source_type="text",
                num=num_q,
                custom_instructions="Generate a mix of MCQs, True/False, Short and Long Answer questions based on this content.",
            )
            st.session_state["text_result"] = result
            clear_quiz_session_state()

    if "text_result" in st.session_state and mode == "Paste Text Content":
        display_questions(st.session_state["text_result"])
            

elif mode == "Mock Practice (AI-Generated)":
    exam_type = st.selectbox("🎯 Choose Mock Exam Style", ["NEET", "JEE", "Class 10", "Class 12"])
    subject = st.text_input("📘 Enter Subject", placeholder="e.g., Biology")
    topic = st.text_input("📚 Optional Topic", placeholder="e.g., Genetics")
    num_q = st.slider("🎯 Number of Mock Questions", 5, 30, 10)

    if st.button("🎲 Generate Mock PYQs") and subject:
        with st.spinner("Generating fresh questions with Gemini..."):
            topic_query = f"{exam_type} {subject} {topic}"
            result = client.qna_engine.generate_questions(
                topic=topic_query,
                num=num_q,
                custom_instructions="Generate diverse PYQ-style MCQ, TF, Short and Long answer questions with explanations, Bloom's levels, and difficulty rating."
            )
            st.session_state["mock_result"] = result 
            clear_quiz_session_state()  

    if "mock_result" in st.session_state and mode == "Mock Practice (AI-Generated)":
        display_questions(st.session_state["mock_result"])

st.divider()
st.subheader("🧠 Doubt Solver")
doubt_img = st.file_uploader("📷 Upload Image of Your Doubt", type=["jpg", "jpeg", "png"])
doubt_prompt = st.text_input("📝 Enter Specific Doubt Prompt (Optional)", placeholder="Explain this diagram in detail")

if st.button("🤖 Solve Doubt") and doubt_img:
    with st.spinner("Analyzing your doubt..."):
        img_path = "temp_doubt.png"
        with open(img_path, "wb") as f:
            f.write(doubt_img.read())

        explanation = client.qna_engine.solve_doubt(
            image_source=img_path,
            prompt=doubt_prompt or "Explain this image in detail",
            detail_level="High"
        )

        st.success("✅ Doubt Solved!")
        st.markdown(f"**Explanation:**\n{explanation.explanation}")
        if explanation.steps:
            st.markdown("**Steps:**")
            for i, step in enumerate(explanation.steps, 1):
                st.markdown(f"{i}. {step}")
        if explanation.additional_notes:
            st.markdown(f"**Additional Notes:**\n{explanation.additional_notes}")

st.caption("✨ PYQ-to-Prep powered by EduChain + Gemini Flash · With Interactive Quizzes & Doubt Solver")
