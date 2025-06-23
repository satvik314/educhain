import streamlit as st
import json

st.set_page_config(page_title="Educhain Verifier", page_icon="📜", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #f0f6ff;
    }
    .title {
        color: #003366;
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        padding: 20px 0;
    }
    .certificate-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎓 Educhain Certificate Verifier</div>', unsafe_allow_html=True)

mode = st.radio("Choose Input Method", ["📤 Upload Certificate JSON", "✍️ Manual Entry"])

cert_data = {}

if mode == "📤 Upload Certificate JSON":
    uploaded_file = st.file_uploader("Upload Certificate JSON", type="json")
    if uploaded_file:
        try:
            cert_data = json.load(uploaded_file)
        except Exception:
            st.error("⚠️ Invalid JSON file.")
elif mode == "✍️ Manual Entry":
    with st.form("manual_entry"):
        name = st.text_input("👤 Full Name")
        course = st.text_input("📘 Course Name")
        issuer = st.text_input("🏫 Issuer (e.g., Educhain)")
        signature = st.selectbox("🔏 Signature", ["valid", "invalid"])
        submitted = st.form_submit_button("Verify Certificate")
        if submitted:
            cert_data = {
                "name": name,
                "course": course,
                "issuer": issuer,
                "signature": signature
            }

if cert_data:
    st.markdown("### 📄 Certificate Preview")
    st.markdown(
        f"""
        <div class="certificate-box">
            <p><b>Name:</b> {cert_data.get("name", "N/A")}</p>
            <p><b>Course:</b> {cert_data.get("course", "N/A")}</p>
            <p><b>Issuer:</b> {cert_data.get("issuer", "N/A")}</p>
            <p><b>Signature:</b> {cert_data.get("signature", "N/A")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if cert_data.get("issuer") == "Educhain" and cert_data.get("signature") == "valid":
        st.success("✅ Certificate is verified!")
        st.balloons()
    else:
        st.error("❌ Certificate is invalid or untrusted.")
