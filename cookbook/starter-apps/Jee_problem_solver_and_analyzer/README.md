# 📚 JEE Advanced Problem Solver & Analyzer  
A lightning-fast, AI-powered assistant that dissects **JEE Advanced** problems straight from an image, powered by **GPT-5 + [Educhain](https://github.com/satvik314/educhain)**.

![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B.svg)
![OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI-black.svg)
![Educhain](https://img.shields.io/badge/Integrated-Educhain-24A148.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🌟 Features
- 📸 **Image Upload**: Drop a JEE Advanced image  
- 🔍 **Topic Extraction**: Instantly see all concepts involved  
- 🧮 **Step-by-Step Solution**: High-detail, exam-grade explanations  
- 🐳 **Similar practice problems**: 5 new problems which use similar concept as the given problem   
- ⚙️ **GPT-5 Engine**: state-of-the-art reasoning  
---

## 🚀 Quick Start

### 1. Clone & Enter
```bash
git clone https://github.com/<your-org>/jee-gpt5-solver.git
cd jee-gpt5-solver
```

### 2. Install Dependencies
```bash
# Using pip
pip install -r requirements.txt

# or modern Python
pip install .
```

> Requirements are **Python ≥3.13**.  
> `uv venv` or standard `venv` is recommended.

### 3. Launch Streamlit
```bash
streamlit run app.py
```
Your browser will open at *http://localhost:8501*.

---

## 🔐 Configure OpenAI Key
- In the sidebar paste your **OpenAI API Key** (Have credits ready; GPT-5 usage applies).  
- The key is **never stored**—it only lives in memory during the session.

---

## 📷 How It Works
1. **Menu (left)**: Enter API key  
2. **Center**: Drop an image (`jpg`, `png`, `jpeg`)  
3. **Click** “Analyze Problem”  
   → Topics appear as 🟢 bullets  
   → Complete solution auto-expands below  

---

## 🛠️ Tech Stack

| Layer           | Tech                        |
|-----------------|-----------------------------|
| LLM Engine      | GPT-5 via `langchain-openai`|
| Orchestration   | Educhain (`educhain`)        |
| UI              | Streamlit (responsive, light & dark modes) |
| Image Support   | Pillow (PIL)                |
| Packaging       | `pyproject.toml` → `pip`,`uv`  |

---


## 🤝 Contributing
Contributions welcome!  
1. Fork the repo  
2. Create a feature branch  
3. `poetry run pytest` (if tests exist)  
4. Open a pull request 🎉  

If you spot bugs, open an [Issue](https://github.com/<your-org>/jee-gpt5-solver/issues) — attach sample images for faster triage.

---

## 📜 License
MIT © 2024 Build Fast with AI.

---

<p align="center">
  Built with ❤️ by <a href="https://buildfastwithai.com">Build Fast with AI</a>
</p>
