<p align="center">
  <img src="https://github.com/Shubhwithai/educhain/blob/main/images/educhain%20final%20logo.svg" alt="Educhain Logo" width="800" height="400">
</p>

<div align="center">
  
  [![PyPI version](https://badge.fury.io/py/educhain.svg)](https://badge.fury.io/py/educhain)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python Versions](https://img.shields.io/pypi/pyversions/educhain.svg)](https://pypi.org/project/educhain/)
  [![Downloads](https://pepy.tech/badge/educhain)](https://pepy.tech/project/educhain)

</div>

# Educhain 🎓🔗
[Website](https://educhain.in) | [Documentation](docs/index.md) | [Migration Guide](MIGRATION.md)

Educhain is a powerful Python package that uses generative AI to create engaging, personalized educational content — multiple-choice questions, lesson plans, study guides, flashcards, podcasts and content built on **8 pedagogical approaches**.

> ### ✨ Educhain 1.0 — now built on the OpenAI SDK
> Educhain 1.0 is a ground-up refresh. **LangChain has been removed** and the
> library now runs directly on the official [OpenAI Python SDK](https://github.com/openai/openai-python).
> That means a lighter install, modern structured outputs, and first-class
> support for **any OpenAI-compatible provider** (OpenAI, Groq, Gemini,
> OpenRouter, Together, Mistral, Cerebras, xAI, Ollama and more).
>
> Upgrading from 0.x? See the **[Migration Guide](MIGRATION.md)**. The old
> method names still work as deprecated aliases.

---

## 🚀 Installation

```bash
pip install educhain
```

The base install is light (just the OpenAI SDK, Pydantic and NumPy) and covers
question generation, all content types, multi-provider support and built-in
RAG. Heavier, optional capabilities live behind extras:

```bash
pip install "educhain[pdf]"      # PDF ingestion + PDF/CSV export
pip install "educhain[youtube]"  # generate questions from YouTube transcripts
pip install "educhain[visual]"   # chart/table questions, image input
pip install "educhain[audio]"    # podcast text-to-speech
pip install "educhain[all]"      # everything
```

Set your API key (OpenAI by default):

```bash
export OPENAI_API_KEY="sk-..."
```

---

## ⚡ Quick Start

```python
from educhain import Educhain

client = Educhain()

mcqs = client.qna.generate(topic="The Water Cycle", num=5)
mcqs.show()
```

That's it. `client.qna` handles questions; `client.content` handles richer
content like lesson plans and study guides.

---

## 🔄 Use Any Provider

Educhain talks to every model through the OpenAI SDK, so any
OpenAI-compatible endpoint works. There are three ways to point it at one:

**1. Named provider presets** (recommended)

```python
from educhain import Educhain

# Reads GROQ_API_KEY from the environment
client = Educhain.from_provider("groq", model="llama-3.3-70b-versatile")

# Google Gemini via its OpenAI-compatible endpoint (reads GEMINI_API_KEY)
client = Educhain.from_provider("gemini", model="gemini-2.0-flash")
```

```python
from educhain import list_providers
print(list_providers())
# anthropic, azure, cerebras, deepinfra, deepseek, fireworks, gemini, groq,
# mistral, nvidia, ollama, openai, openrouter, perplexity, sambanova,
# together, xai
```

**2. A raw base URL + key** for anything not in the registry

```python
from educhain import Educhain, LLMConfig

client = Educhain(LLMConfig(
    model="my-model",
    base_url="https://my-openai-compatible-host/v1",
    api_key="...",
))
```

**3. Bring your own client** (the escape hatch — e.g. Azure)

```python
from openai import AzureOpenAI
from educhain import Educhain

client = Educhain.from_client(
    AzureOpenAI(azure_endpoint="...", api_key="...", api_version="..."),
    model="my-deployment",
)
```

> **How structured output stays reliable across providers:** Educhain first
> tries OpenAI's strict structured outputs (`response_format` with a Pydantic
> schema). If a provider or schema doesn't support that, it automatically falls
> back to JSON mode with local Pydantic validation — you always get a typed
> object back. Control this with `LLMConfig(structured_mode="auto" | "native" | "json")`.

---

## ✨ Features

<details>
<summary>📝 Generate Multiple-Choice Questions</summary>

```python
from educhain import Educhain

client = Educhain()

mcqs = client.qna.generate(
    topic="Solar System",
    num=5,
    difficulty_level="Hard",                 # any extra context is woven in
    custom_instructions="Include recent discoveries",
)
print(mcqs.model_dump_json(indent=2))
```
</details>

<details>
<summary>🔠 Different Question Types</summary>

```python
client.qna.generate(topic="Photosynthesis", num=3, question_type="Multiple Choice")
client.qna.generate(topic="Photosynthesis", num=3, question_type="True/False")
client.qna.generate(topic="Photosynthesis", num=3, question_type="Fill in the Blank")
client.qna.generate(topic="Photosynthesis", num=3, question_type="Short Answer")
```
</details>

<details>
<summary>📁 Generate Questions from Text, PDFs & URLs</summary>

```python
client.qna.generate_from_url("https://en.wikipedia.org/wiki/Photosynthesis", num=5)
client.qna.generate_from_pdf("notes.pdf", num=5)           # needs educhain[pdf]
client.qna.generate_from_text("Long passage of study material...", num=5)
```
</details>

<details>
<summary>📹 Generate Questions from YouTube</summary>

Requires `educhain[youtube]`.

```python
questions = client.qna.generate_from_youtube(
    url="https://www.youtube.com/watch?v=...",
    num=3,
    target_language="en",
)
```
</details>

<details>
<summary>🖼️ Solve Doubts from Images (Vision)</summary>

```python
solution = client.qna.solve_doubt(
    image_source="https://example.com/math-problem.png",
    prompt="Explain how to solve this step by step",
    detail_level="high",
)
solution.show()
```
</details>

<details>
<summary>📊 Visual (Chart-Based) Questions</summary>

Requires `educhain[visual]`.

```python
visual = client.qna.generate_visual(topic="Population growth statistics", num=3)
visual.show()
```
</details>

<details>
<summary>🧮 Math Questions with Verified Answers</summary>

```python
# Each numerical answer is recomputed and turned into clean options.
math_mcqs = client.qna.generate_math(topic="Quadratic equations", num=5)
math_mcqs.show()
```
</details>

<details>
<summary>🔎 Retrieval-Augmented Generation (RAG)</summary>

Built in — no vector database to set up. Educhain chunks the source, embeds it,
and retrieves the most relevant passages before generating.

```python
questions = client.qna.generate_with_rag(
    source="https://en.wikipedia.org/wiki/Climate_change",
    source_type="url",
    num=5,
    learning_objective="Causes and effects of climate change",
)
```
</details>

<details>
<summary>📦 Bulk Generation from a Topic Tree</summary>

```python
result, output_file, total, failed = client.qna.generate_bulk(
    topics_file="topics.json",          # topics -> subtopics -> objectives
    questions_per_objective=5,
    question_type="Multiple Choice",
    output_format="json",
)
print(f"Generated {total} questions -> {output_file}")
```
</details>

<details>
<summary>💾 Export to PDF / CSV</summary>

Requires `educhain[pdf]` for PDF and `educhain[visual]` for CSV.

```python
mcqs, pdf_path = client.qna.generate(topic="History", num=5, output_format="pdf")
mcqs, csv_path = client.qna.generate(topic="History", num=5, output_format="csv")
```
</details>

<details>
<summary>🎨 Custom Prompts & Custom Schemas</summary>

```python
from pydantic import BaseModel
from typing import List

class MyQuestion(BaseModel):
    question: str
    answer: str
    hint: str

class MyQuestionList(BaseModel):
    questions: List[MyQuestion]

result = client.qna.generate(
    topic="Algebra",
    num=3,
    response_model=MyQuestionList,
    prompt_template="Create {num} algebra questions about {topic}, each with a hint.",
)
```
</details>

<details>
<summary>📚 Lesson Plans, Study Guides, Flashcards & Careers</summary>

```python
client.content.lesson_plan(topic="Photosynthesis", grade_level="High School")
client.content.study_guide(topic="World War II", difficulty_level="Intermediate")
client.content.flashcards(topic="Spanish vocabulary", num=20)
client.content.career_connections(topic="Statistics", industry_focus="Data Science")
```
</details>

<details>
<summary>🎓 Pedagogy-Based Content (8 approaches)</summary>

```python
client.content.pedagogy(topic="Fractions", approach="blooms_taxonomy")
client.content.pedagogy(topic="Ethics", approach="socratic_questioning")
client.content.pedagogy(topic="Bridges", approach="project_based_learning")

# Discover approaches and their parameters
print(client.content.list_pedagogies())
# blooms_taxonomy, socratic_questioning, project_based_learning,
# flipped_classroom, inquiry_based_learning, constructivist,
# gamification, peer_learning
```
</details>

<details>
<summary>🎙️ Podcasts (Script + Audio)</summary>

Audio requires `educhain[audio]`.

```python
# Script only
script = client.content.podcast_script(topic="The history of the internet")

# Complete podcast (script + narrated audio file)
podcast = client.content.podcast(
    topic="The history of the internet",
    output_path="podcast.mp3",
    tts_provider="google",
)
```
</details>

<details>
<summary>📈 Track Token Usage</summary>

```python
with client.client.track_usage() as usage:
    client.qna.generate(topic="Biology", num=10)
print(usage)   # requests, prompt/completion/total tokens
```
</details>

---

## 🎓 Pedagogy & Educational Theory

Educhain bakes in eight research-backed teaching approaches so generated
content reflects sound learning design, not just raw text:

| Approach | What it does |
| --- | --- |
| **Bloom's Taxonomy** | Structures content across six cognitive levels |
| **Socratic Questioning** | Guided self-discovery through strategic questions |
| **Project-Based Learning** | Real-world projects that build practical skills |
| **Flipped Classroom** | Pre-class study + active in-class application |
| **Inquiry-Based Learning** | Learning through investigation and discovery |
| **Constructivist** | Knowledge built via experience and reflection |
| **Gamification** | Game mechanics to drive engagement |
| **Peer Learning** | Structured student collaboration |

---

## 📦 Architecture

```
educhain/
├── core/         Educhain client, LLMConfig, LLMClient (structured-output engine)
├── providers/    Registry of OpenAI-compatible providers
├── engines/      QnAEngine + ContentEngine
├── models/       Pydantic models for every content type
└── utils/        Loaders, text splitter, in-memory vector store, formatters, TTS
```

---

## 🛠 Development

```bash
git clone https://github.com/satvik314/educhain.git
cd educhain
pip install -e ".[all,dev]"
pytest
```

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

Educhain is released under the [MIT License](LICENSE).
