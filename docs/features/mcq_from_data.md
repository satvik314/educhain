# 📝 Multiple Choice Question (MCQ) Generation from Data

Generate engaging MCQs from various data sources using AI! 🧠✨

## 🚀 Basic Usage

```python
from educhain import generate_mcqs_from_data

questions = generate_mcqs_from_data(
    source="https://en.wikipedia.org/wiki/Artificial_intelligence",
    source_type="url",
    num=5,
    learning_objective="Understand the basics of AI",
    difficulty_level="Intermediate"
)

questions.show()
```

## 🎛️ Customization Options

| Option | Description | Example Values |
|--------|-------------|----------------|
| `source` | Data source for question generation | PDF file path, URL, or text content |
| `source_type` | Type of the data source | "pdf", "url", "text" |
| `num` | Number of questions to generate | 5, 10, 20 |
| `learning_objective` | Goal of the questions | "Understand AI basics", "Apply ML concepts" |
| `difficulty_level` | Difficulty of the questions | "Beginner", "Intermediate", "Advanced" |
| `llm` | Custom language model (optional) | ChatOpenAI(model="gpt-4") |
| `prompt_template` | Custom prompt template (optional) | "Generate questions about {topic}..." |

## 📊 Output Format

```python
MCQList(
    questions=[
        MCQ(
            question="What is artificial intelligence primarily concerned with?",
            options=[
                "Creating intelligent machines",
                "Developing faster computers",
                "Improving internet connectivity",
                "Designing user interfaces"
            ],
            correct_answer="Creating intelligent machines",
            explanation="Artificial intelligence focuses on creating machines that can perform tasks requiring human-like intelligence."
        ),
        # More questions...
    ]
)
```

## 🌟 Pro Tips

- Use specific URLs or PDF content for more focused questions
- Adjust the `learning_objective` and `difficulty_level` to match your audience
- Experiment with custom prompt templates for specialized question generation

## 📚 Supported Data Sources

1. **PDF Files** 📄: Provide a file path to generate questions from PDF content.
2. **URLs** 🌐: Input a web page URL to create questions from online content.
3. **Text** 📝: Directly input text to generate questions from custom content.

Ready to create MCQs from your own data? Start generating now! 🚀📚
