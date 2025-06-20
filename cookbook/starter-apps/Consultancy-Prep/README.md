# 🧩 Consulting Interview Prep App

An AI-powered Streamlit application designed to simplify and personalize consulting interview preparation. This app leverages the **Educhain SDK** and **Gemini LLM** to generate tailored MCQs, consulting frameworks, and guesstimate problems from manual prompts, PDFs, or website URLs.

---

## 🚀 Features

* **Multiple Input Options:** Manual Prompt, PDF Upload, Website URL
* **MCQ Generation:** Auto-generated Multiple Choice Questions with difficulty levels
* **Consulting Framework Generation:** Structured problem-solving frameworks via Gemini LLM
* **Guesstimate Problem Generator:** Realistic guesstimate cases and solution approach
* **Difficulty Selector:** Beginner, Intermediate, Advanced
* **Streamlit Frontend:** Clean, interactive user interface

---

## 🔧 Tech Stack

* **Python 3.9+**
* [Streamlit](https://streamlit.io/)
* [Educhain SDK](https://pypi.org/project/educhain/)
* [Langchain Google Gemini](https://pypi.org/project/langchain-google-genai/)

---

## ⚙️ Setup Instructions

### 1. Clone this Repository

```bash
git clone https://github.com/yourusername/consulting-prep-app.git
cd consulting-prep-app
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Google API Key

* Add your **Google Gemini API key** in Streamlit Cloud Secrets or `.env` if running locally:

```
GOOGLE_API_KEY=your-api-key-here
```

Or use Streamlit Cloud's Secrets Manager.

### 5. Run the App

```bash
streamlit run app.py
```

App will be available at `http://localhost:8501`.

---

## 📄 Input Options

* **Manual Prompt:** Enter any business case prompt.
* **PDF Upload:** Upload a casebook or document.
* **Website URL:** Provide a valid URL for case extraction.

---

## 💡 Future Development

* Auto MCQ scoring and evaluation
* AI-powered mock interviews
* Case library by consulting firms (McKinsey, BCG, Bain)
* Mobile-friendly version
* Real-time data integration for fresh market cases

---

## 🤝 Credits

Built with ❤️ using **Educhain SDK**, **Gemini LLM**, and **Streamlit**.

---
