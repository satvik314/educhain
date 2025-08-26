# 🧠 Educhain Pedagogy

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.13+-3776ab.svg)](https://www.python.org/downloads/)
[![JavaScript](https://img.shields.io/badge/TypeScript-Next.js-3178c6.svg)](https://nextjs.org/docs)
[![FastAPI](https://img.shields.io/badge/-FastAPI-009485.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4-06b6d4.svg)](https://tailwindcss.com)


Generate tailored, style-specific learning experiences across 8 pedagogical approaches—powered by Educhain + GPT-4o.

<br/>

---

## 🧩 Pedagogies Supported
- Blooms Taxonomy 🎓
- Socratic Questioning 🧠
- Project Based Learning 🧩
- Flipped Classroom 🔁
- Inquiry Based Learning 🔎
- Constructivist 🏗️  
- Gamification 🎮
- Peer Learning 🤝
- Game-Based Learning 🎮


---

## ⚡ Quickstart

### 1. Prerequisites
- **Python 3.13+** & **uv** (or pip)
- Node.js ≥ 20 & **pnpm** or **npm**

```bash
# install uv if you don’t have it
pip install uv
```

### 2. Clone & install

```bash
git clone https://github.com/YOUR_ORG/educhain-pedagogy.git
cd educhain-pedagogy

# backend
cd backend
`uv add -r requirements.txt `   or `pip install -r requirements.txt`

 de                 # or `npm install`
```

> The project uses **git-locked Educhain** (`ai-dev` branch). No extra config needed.

### 3. Run locally

#### Backend
```bash
uv run uvicorn main:app --reload   # http://localhost:8000
```

#### Frontend
```bash
npm run dev                       # http://localhost:3000
```

### 4. Environment 
A `.env` in `backend/` is automatically loaded via `dotenv`.  
Only required key:
```
OPENAI_API_KEY=sk-XXXXXXXX
```
### 5 . Backend url in frontend 
In `frontend/src/lib/_app.jsx`, set the backend URL of your backend deployment (or `http://localhost:8000` for local dev):
```

---

## 🛠️ Tech Stack

| Layer        | Stack                                                      |
|--------------|-----------------------------------------------------------|
| Backend      | Python, FastAPI, Educhain (GPT-4o), Pydantic              |
| Frontend     | Next.js 15, TailwindCSS 4, React 19, Axios, Lucide Icons  |
| Package Mgmt | uv (Python) & npm (Node)                                 |
| Deployment   | Render (free tier)      , Vercel                           |

---

## 📘 API Usage Examples

### 1. List available pedagogies
```bash
curl https://educhain-pedagogy.onrender.com/available-pedagogies
```

### 2. Generate content
```bash
curl -X POST https://educhain-pedagogy.onrender.com/generate-content \
  -H "Content-Type: application/json" \
  -d '{
        "topic": "Photosynthesis in Grade 8",
        "pedagogy": "blooms_taxonomy",
        "params": {
          "grade_level": "8th Grade",
          "target_level": "Intermediate"
        }
      }'
```

---

## 📁 Project Structure

```
educhain-pedagogy/
├── backend/
│   ├── main.py
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   └── services/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── lib/
│   │   └── pages/
│   └── next.config.js
└── README.md
```

---

## 🤝 Contributing

1. Fork the repository  
2. Create a feature branch: `git checkout -b feat/<feature-name>`  
3. Commit & push: `git commit -m 'feat: added ____'`  
4. Open a Pull Request 🎉


