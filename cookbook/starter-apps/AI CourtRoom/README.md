# ⚖️ AI Courtroom

[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://github.com/your-org/ai-courtroom)  
[![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-FF4B4B.svg?logo=streamlit)](https://streamlit.io)  
[![Cerebras](https://img.shields.io/badge/-Cerebras-000000.svg?logo=fastapi)](https://cerebras.ai)  
[![Python](https://img.shields.io/badge/Python-3.13+-3776ab.svg?logo=python&logoColor=white)](https://python.org)  
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)  

---

### 🔍 What is AI Courtroom?
AI Courtroom is a **fully-automated mock-trial simulator** that ingests real legal cases from the web, extracts key facts using **Educhain + Cerebras AI**, and role-plays a multi-character courtroom (Judge ⚖️ → Prosecutor ⚔️ → Defense 🛡️ → Defendant 👤 → Verdict 🔨) in the style you choose—**Serious**, **Dramatic**, or outright **Comedic**.

Just paste a Wikipedia article, news report, blog post, or any other case URL and watch the AI attorneys battle it out in seconds.

---

## 🚀 Quick Start

| Requirement | Command |
|-------------|---------|
| Python | ≥ 3.13 |
| OS | macOS / Linux / Windows (WSL) |

### 1. Clone & enter the repo
```bash
git clone https://github.com/your-org/ai-courtroom.git
cd ai-courtroom
```

### 2. Create & activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt        # pip
# OR (if you have pyproject.toml):
# poetry install
```

### 4. Get a Cerebras API key
1. Sign up at [Cerebras AI](https://cerebras.ai)
2. Copy your key from the dashboard
3. (Optional) Store it as an env variable:  
   ```bash
   export CEREBRAS_API_KEY="cks_××××××"
   ```

### 5. Launch the app
```bash
streamlit run app.py
```
A browser tab will open at `http://localhost:8501`.

---

## 🖥️ Usage
1. **Sidebar** → paste your **Cerebras API key**  
2. Pick **Courtroom style** (Serious, Dramatic or Comedic)  
3. Set the **number of facts/questions** to extract (1 – 10)  
4. **Paste the URL** to any public legal case (Wikipedia, news, court filings, etc.)  
5. Click **“Ingest case & generate facts”**  
6. Sit back & watch the AI roles rehearse the case live.

---

## 🧱 Tech Stack

| Layer | Tech | Purpose |
|-------|------|---------|
| **Frontend** | Streamlit | Interactive web UI |
| **LLM Core** | Cerebras `gpt-oss-120b` | Lightning-fast inference |
| **NLP Chain** | EduChain | Auto-Q&A & fact extraction |
| **Python Version** | ≥ 3.13 | All major deps compiled for it |
| **Dependency Mgmt** | `requirements.txt` & `pyproject.toml` | Pip or Poetry ready |

---

## 🛠️ Development & Contribution

### Pull-Request flow
1. Fork the repo  
2. Create a feature branch: `git checkout -b feat/amazing-idea`  
3. Commit meaningful messages (`feat:`, `fix:`, `chore:` prefixes)  
4. Run the lint & test helpers (if any are added)  
   ```bash
   pre-commit run --all-files
   pytest   # optional future addition
   ```
5. Push & open a PR against `main`.  
Every PR is auto-checked by the status badge at the top of this file.

### Local dev tips
- Use `streamlit run app.py --server.port=3000` to bind a custom port.
- Set `STREAMLIT_THEME_BASE="dark"` in `.env` for a slick dark mode.

---

## 📦 Project Structure
```
ai-courtroom
├─ app.py              # Main Streamlit entry
├─ requirements.txt    # Quick install with pip
├─ pyproject.toml      # Poetry / PEP-621 compliant spec
└─ README.md           # This file
```

---

## 📄 License
MIT © [Build Fast with AI](https://buildfastwithai.com)

---

**Want to showcase this?**  
The repo is ready for **Render**/**Railway** deployments using one-click buttons—just switch the runtime version to `3.13-slim` and inject `CEREBRAS_API_KEY` as an **environment variable** in the deployment dashboard.