# Migrating to Educhain 1.0

Educhain 1.0 is a ground-up refresh. **LangChain has been removed** and the
library now runs directly on the official OpenAI Python SDK. This brings a
lighter install, modern structured outputs, and native support for any
OpenAI-compatible provider.

This guide covers everything you need to upgrade from 0.x.

> **Good news:** the old method names still work as **deprecated aliases**, so
> most existing code keeps running (with a `DeprecationWarning`). You can
> migrate at your own pace.

---

## 1. Installation

LangChain and ChromaDB are gone. The base install is much lighter; heavier
features are now optional extras.

```bash
pip install --upgrade educhain        # core

# add only what you need:
pip install "educhain[pdf]"           # PDF ingestion + PDF/CSV export
pip install "educhain[youtube]"       # YouTube transcripts
pip install "educhain[visual]"        # chart/table questions, image input
pip install "educhain[audio]"         # podcast TTS
pip install "educhain[all]"           # everything
```

If you previously relied on PDF, YouTube, visual or audio features, install the
matching extra. Educhain raises a clear, actionable error if an extra is
missing.

---

## 2. The client and engines

The `Educhain` entry point is unchanged, but the engines now have shorter
names. The old names remain as aliases.

| 0.x | 1.0 |
| --- | --- |
| `client.qna_engine` | `client.qna` *(old name still works)* |
| `client.content_engine` | `client.content` *(old name still works)* |

```python
from educhain import Educhain

client = Educhain()
client.qna.generate("Photosynthesis", num=5)        # new
client.qna_engine.generate_questions("...", num=5)  # still works (deprecated)
```

---

## 3. Method renames

All generation methods got cleaner, verb-first names. **Old names are kept as
deprecated aliases** and forward to the new ones.

### QnA engine

| 0.x | 1.0 |
| --- | --- |
| `generate_questions(...)` | `generate(...)` |
| `generate_questions_from_data(source, source_type, ...)` | `generate_from_source(...)` — or `generate_from_text/pdf/url(...)` |
| `generate_questions_from_youtube(...)` | `generate_from_youtube(...)` |
| `generate_visual_questions(...)` | `generate_visual(...)` |
| `generate_mcq_math(...)` | `generate_math(...)` |
| `generate_questions_with_rag(...)` | `generate_with_rag(...)` |
| `bulk_generate_questions(topic=...)` | `generate_bulk(topics_file=...)` |

### Content engine

| 0.x | 1.0 |
| --- | --- |
| `generate_lesson_plan(...)` | `lesson_plan(...)` |
| `generate_study_guide(...)` | `study_guide(...)` |
| `generate_career_connections(...)` | `career_connections(...)` |
| `generate_flashcards(...)` | `flashcards(...)` |
| `generate_pedagogy_content(topic, pedagogy=...)` | `pedagogy(topic, approach=...)` |
| `get_available_pedagogies()` | `list_pedagogies()` |
| `generate_podcast_script(...)` | `podcast_script(...)` |
| `generate_podcast_from_script(...)` | `podcast_from_script(...)` |
| `generate_complete_podcast(...)` | `podcast(...)` |

---

## 4. Configuration & providers

This is the biggest change. In 0.x you switched models by passing a LangChain
chat model as `custom_model`. In 1.0 there is no LangChain — you use provider
presets, a base URL, or your own OpenAI client.

### Before (0.x)

```python
from educhain import Educhain, LLMConfig
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="...")
client = Educhain(LLMConfig(custom_model=gemini))

groq = ChatOpenAI(model="llama-3.3-70b", base_url="https://api.groq.com/openai/v1", api_key="...")
client = Educhain(LLMConfig(custom_model=groq))
```

### After (1.0)

```python
from educhain import Educhain, LLMConfig

# Option A: provider presets (reads the provider's API-key env var)
client = Educhain.from_provider("gemini", model="gemini-2.0-flash")
client = Educhain.from_provider("groq", model="llama-3.3-70b-versatile")

# Option B: any OpenAI-compatible base URL
client = Educhain(LLMConfig(model="llama-3.3-70b",
                            base_url="https://api.groq.com/openai/v1",
                            api_key="..."))

# Option C: bring your own pre-built OpenAI client (e.g. Azure)
from openai import OpenAI
client = Educhain.from_client(OpenAI(base_url="...", api_key="..."), model="...")
```

### `LLMConfig` field changes

| 0.x | 1.0 |
| --- | --- |
| `model_name="gpt-4o-mini"` | `model="gpt-4o-mini"` *(old kwarg still works, warns)* |
| `custom_model=<langchain model>` | `provider=...` / `base_url=...` / `client=<openai client>` |
| `api_key`, `base_url`, `temperature`, `max_tokens`, `default_headers` | unchanged |
| — (new) | `provider`, `structured_mode`, `embedding_model`, `timeout`, `max_retries` |

`LLMConfig(model_name=...)` and `LLMConfig(custom_model=<openai client>)` still
work for now but emit a `DeprecationWarning`.

---

## 5. Structured output

0.x used LangChain's `PydanticOutputParser` and injected "format instructions"
into every prompt. 1.0 uses the OpenAI SDK's structured outputs directly and
chooses the best strategy automatically:

- **native** — `chat.completions.parse` with your Pydantic model (strict schema).
- **json** — JSON mode + local Pydantic validation (works on any provider, and
  on schemas that strict mode can't represent, e.g. free-form `dict` fields).

In the default `"auto"` mode Educhain tries native first and transparently falls
back to json. Override it if you like:

```python
LLMConfig(model="gpt-4o-mini", structured_mode="json")
```

You still get the same Pydantic objects back — `MCQList`, `StudyGuide`, etc.

---

## 6. RAG: no more ChromaDB

`generate_with_rag` no longer needs ChromaDB or a LangChain agent. Educhain now
ships a built-in, dependency-free retriever (a NumPy in-memory vector store over
OpenAI embeddings). The public call is essentially the same:

```python
client.qna.generate_with_rag(
    source="https://example.com/article",
    source_type="url",
    num=5,
    learning_objective="...",
)
```

Tune retrieval with `k`, `chunk_size`, `chunk_overlap` and `retrieval_query`.

---

## 7. Models are unchanged

All Pydantic models (`MCQList`, `LessonPlan`, `StudyGuide`, `FlashcardSet`,
pedagogy models, podcast models, …) keep the same fields and `.show()` helpers,
so any code that reads results continues to work.

---

## Questions?

Open an issue at https://github.com/satvik314/educhain/issues.
