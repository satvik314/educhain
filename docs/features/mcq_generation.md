
# 🧠 Educhain Usage

Leverage Educhain's flexibility to generate customized content with ease! 🌟

---

## 🚀 Basic Usage

```python
from educhain import Educhain

# Initialize Educhain client
client = Educhain()

# Generate "Fill in the Blank" questions with custom instructions
ques = client.qna_engine.generate_questions(
    topic="Psychology",
    num=10,
    question_type="Fill in the Blank",
    custom_instructions="Only basic questions"
)

# Supported question types: "Multiple Choice" (default), "True/False", "Fill in the Blank", "Short Answer"
print(ques)
```

---

## 🌟 Advanced LLM Integration

Use custom LLM models like Google's Gemini with Educhain for enhanced content generation! 🚀✨

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from educhain import Educhain, LLMConfig

# Configure Gemini model
gemini_flash = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-exp-0827",
    google_api_key="GOOGLE_API_KEY"
)

# Set up LLM configuration
flash_config = LLMConfig(custom_model=gemini_flash)

# Initialize Educhain with Gemini
client = Educhain(flash_config)

# Generate questions using Gemini-powered Educhain
ques = client.qna_engine.generate_questions(
    topic="Psychology",
    num=10
)

print(ques)
```

---

## 🌟 Pro Tips

- Experiment with `custom_instructions` to tailor questions to specific needs.
- Use `LLMConfig` to integrate third-party models for diverse use cases.

Ready to take Educhain to the next level? Start exploring today! 🚀✨
```
