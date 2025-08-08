from langchain_openai import ChatOpenAI
import streamlit as st
from educhain import Educhain, LLMConfig
from PIL import Image
import os

# Initialize Educhain client
def initialize_educhain(api_key):
    openai_model = ChatOpenAI(
        model_name="gpt-5",  # Use GPT-5 model
        openai_api_key=api_key,
        temperature=1  # Adjust temperature if needed
    )
    openai_config = LLMConfig(custom_model=openai_model)
    client = Educhain(openai_config)
    return client

# Main Streamlit app
def main():
    st.set_page_config(page_title="JEE GPT-5 Solver", layout="wide")
    st.title("📚 JEE Advanced Problem Solver and Analyzer")
    st.subheader("⭐ GPT-5 X Educhain ⭐")

    # Sidebar
    with st.sidebar:
        st.markdown(
            "<div style='text-align: center; margin: 2px 0;'>"
            "<a href='https://www.buildfastwithai.com/' target='_blank' style='text-decoration: none;'>"
            "<div style='border: 2px solid #e0e0e0; border-radius: 6px; padding: 4px; "
            "background: linear-gradient(145deg, #ffffff, #f5f5f5); "
            "box-shadow: 0 2px 6px rgba(0,0,0,0.1); "
            "transition: all 0.3s ease; display: inline-block; width: 100%;'>"
            "<img src='https://github.com/Shubhwithai/chat-with-qwen/blob/main/company_logo.png?raw=true' "
            "style='width: 100%; max-width: 100%; height: auto; border-radius: 8px; display: block;' "
            "alt='Build Fast with AI Logo'>"
            "</div></a></div>", unsafe_allow_html=True
        )

        st.header("🔐 API Settings")
        api_key = st.text_input("Enter your OpenAI API Key", type="password")
        st.markdown("---")
        st.markdown("⭐ Model: `GPT-5`")
        st.markdown("---")
        st.markdown("""<div class="sidebar-footer">
                <p>❤️ Built by <a href="https://buildfastwithai.com" target="_blank">Build Fast with AI</a></p>
            </div> """, unsafe_allow_html=True)

    if not api_key:
        st.warning("Please enter your OpenAI API Key in the sidebar.")
        st.stop()

    # Initialize Educhain client
    client = initialize_educhain(api_key)

    # File upload section
    st.header("📷 Upload JEE Advanced Problem Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Save the uploaded image to a temporary file
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        image = Image.open(temp_image_path)
        st.image(image, caption="Problem Image", use_container_width=True)

        if st.button("Analyze Problem"):
            with st.spinner("Analyzing the problem..."):
                try:
                    # Step 1: Extract topics
                    topics_response = client.qna_engine.solve_doubt(
                        image_source=temp_image_path,
                        prompt="List all the topics used in this JEE Advanced problem.",
                        detail_level="High"
                    )
                    raw_topics = getattr(topics_response, 'explanation', "No topics found.")
                    st.subheader("📚 Topics Involved")

                    # Clean topic output into bullet list
                    topic_lines = [t.strip("-•\n ") for t in raw_topics.splitlines() if t.strip()]
                    if topic_lines:
                        for topic in topic_lines:
                            st.markdown(f"- {topic}")
                    else:
                        st.markdown("No topics found.")

                    # Step 2: Generate full solution
                    solution_response = client.qna_engine.solve_doubt(
                        image_source=temp_image_path,
                        prompt="Provide a detailed solution for this JEE Advanced problem.",
                        detail_level="High"
                    )
                    solution = getattr(solution_response, 'explanation', "No solution found.")
                    steps = getattr(solution_response, 'steps', [])
                    notes = getattr(solution_response, 'additional_notes', "No additional notes.")
                    st.markdown("---")
                    st.subheader("🧠 Detailed Solution")
                    st.markdown(solution)

                    st.markdown("#### 📌 Step-by-Step Breakdown")
                    if steps:
                        for i, step in enumerate(steps, start=1):
                            st.markdown(f"**Step {i}:** {step}")
                    else:
                        st.markdown("_No individual steps found._")

                    st.markdown("#### 🗒️ Additional Notes")
                    st.markdown(notes)

                    # Step 3: Generate practice questions
                    practice_questions_response = client.qna_engine.generate_questions(
                        topic=raw_topics,
                        num=5,
                        question_type="Multiple Choice",
                        custom_instructions="Generate practice questions based on the same concept."
                    )
                    questions = getattr(practice_questions_response, 'questions', [])
                    st.markdown("---")
                    st.subheader("📝 Practice Questions")
                    for idx, question in enumerate(questions, start=1):
                        st.markdown(f"**Question {idx}:** {question.question}")

                        st.markdown("**Options:**")
                        for option in question.options:
                            st.markdown(f"- {option}")

                        st.markdown(f"**Answer:** {question.answer}")
                        st.markdown("**Explanation:**")
                        st.markdown(question.explanation)
                        st.markdown("---")

                except Exception as e:
                    st.error(f"❌ An error occurred:\n\n{e}")

            # Clean up temporary image
            os.remove(temp_image_path)


if __name__ == "__main__":
    main()
