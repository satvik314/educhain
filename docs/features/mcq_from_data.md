# 🖋️ Multiple Choice Question (MCQ) Generation from Data

Generate engaging MCQs from various data sources using AI! 🧠✨

## 🚀 Basic Usage

```python
from educhain import Educhain

client = Educhain()

# From URL
url_questions = client.qna_engine.generate_questions_from_data(
    source="https://example.com/article",
    source_type="url",
    num=3
)

# From PDF
pdf_questions = client.qna_engine.generate_questions_from_data(
    source="path/to/document.pdf",
    source_type="pdf",
    num=3
)

# From Text File
text_questions = client.qna_engine.generate_questions_from_data(
    source="path/to/content.txt",
    source_type="text",
    num=3
)
```

## 🎡 Function Parameters

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `source` | Data source for question generation | PDF file path, URL, or text content |
| `source_type` | Type of the data source | "pdf", "url", "text" |
| `num` | Number of questions to generate | 5, 10, 20 |
| `question_type` | Type of questions to generate | "Multiple Choice", "True/False" |
| `prompt_template` | Custom prompt template (optional) | "Generate questions about {topic}..." |
| `custom_instructions` | Additional instructions for question generation (optional) | "Focus on technical details." |
| `response_model` | Custom response model (optional) | CustomModelClass |
| `output_format` | Format for the output questions (optional) | "JSON", "PDF", "Text" |

## 🖋️ Example Output

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

## 🌍 Supported Data Sources

1. **PDF Files** 📄: Provide a file path to generate questions from PDF content.
2. **URLs** 🌐: Input a web page URL to create questions from online content.
3. **Text Files** 🖋️: Provide text files for generating questions from custom content.

## ✨ Advanced Customization

Enhance your MCQ generation with additional customization:

- **Custom Prompt Templates:** Use the `prompt_template` parameter to provide specific instructions.
- **Fine-Tune Outputs:** Leverage `custom_instructions` to focus on particular aspects of the source content.
- **Flexible Output Formats:** Choose between JSON, PDF, or plain text for your generated questions.


## 📊 Pro Tips

- **Refine the Source Content:** Use specific URLs or curated text for targeted question generation.
- **Optimize Learning Objectives:** Adjust the `learning_objective` to align with your educational goals.
- **Experiment with Difficulty Levels:** Tailor `difficulty_level` to your audience, ranging from "Beginner" to "Advanced."

Ready to create high-quality MCQs? Dive in and let Educhain streamline your educational content creation! 🚀📚

