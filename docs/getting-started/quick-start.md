## 🏃‍♂️ getting-started/quick-start.md

```markdown
# 🏃‍♂️ Quick Start Guide

Get up and running with Educhain in minutes! 🚀

## 📚 Basic Usage

Here's a simple example to generate multiple-choice questions:

```python
from educhain import qna_engine

questions = qna_engine.generate_mcq(
    topic="Python Programming",
    level="Beginner",
    num=5
)

for i, q in enumerate(questions, 1):
    print(f"Question {i}: {q['question']}")
    for j, option in enumerate(q['options'], 1):
        print(f"  {j}. {option}")
    print(f"Correct Answer: {q['correct_answer']}\n")
```

## 🔧 Customization

Customize your questions with additional parameters:

```python
questions = qna_engine.generate_mcq(
    topic="Machine Learning",
    level="Intermediate",
    num=3,
    question_type="conceptual",
    language="English"
)
```

## 📊 Generating Lesson Plans

Create comprehensive lesson plans with ease:

```python
from educhain import content_engine

lesson_plan = content_engine.generate_lesson_plan(
    topic="World War II",
    grade_level="High School",
    duration="60 minutes"
)

print(lesson_plan)
```

## 🎉 Next Steps

- Explore [📝 MCQ Generation](../features/mcq-generation.md) in depth
- Learn about [📊 Lesson Plan Generation](../features/lesson-plans.md)
- Check out [🔢 Different Question Types](../features/question-types.md)

Happy learning with Educhain! 🎓✨
```

## ⚙️ getting-started/configuration.md

```markdown
# ⚙️ Configuration

Customize Educhain to fit your needs perfectly! 🎛️

## 🔑 API Key Configuration

Set your OpenAI API key:

```python
import educhain

educhain.api_key = "your-api-key-here"
```

Or use an environment variable:

```bash
export EDUCHAIN_API_KEY="your-api-key-here"
```

## 🌐 Language Model Selection

Choose your preferred language model:

```python
from educhain import qna_engine

qna_engine.set_model("gpt-4")  # Default is "gpt-4o-mini"
```

## 🎨 Customizing Prompt Templates

Define your own prompt templates:

```python
from educhain import qna_engine

custom_template = """
Generate {num} multiple-choice questions about {topic} at {level} level.
Each question should have 4 options and one correct answer.
"""

qna_engine.set_prompt_template(custom_template)
```



## 🎉 Next Steps

- Explore [🔬 Advanced Usage](../advanced-usage/custom-prompts.md)
- Learn about [🤖 Different LLM Models](../advanced-usage/llm-models.md)
- Check out our [💡 Best Practices](../guides/best-practices.md)

Need more help? Join our [💬 Discord community](https://discord.gg/educhain)!
```
