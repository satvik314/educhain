# Educhain 🎓🔗

[![PyPI version](https://badge.fury.io/py/educhain.svg)](https://badge.fury.io/py/educhain)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/educhain.svg)](https://pypi.org/project/educhain/)
[![Downloads](https://pepy.tech/badge/educhain)](https://pepy.tech/project/educhain)

[Website](https://educhain.in) | [Documentation](docs/index.md) | 

Educhain is a powerful Python package that leverages Generative AI to create engaging and personalized educational content. From generating multiple-choice questions to crafting comprehensive lesson plans, Educhain makes it easy to apply AI in various educational scenarios.

<img src="images/logo.svg" alt="Educhain Logo" align="center" height = 120 width = 120 />

## 🚀 Features

- 📝 Generate Multiple Choice Questions (MCQs)
- 📊 Create Lesson Plans
- 🔄 Support for various LLM models
- 📁 Export questions to JSON, PDF, and CSV formats
- 🎨 Customizable prompt templates
- 📚 Generate questions from text/PDF files

## 📈 Performance

Educhain consistently outperforms traditional methods in content generation speed and quality:

<img src="images\educhain-comparison-svg.svg" alt="Performance Comparison Graph" />

## 🛠 Installation

```bash
pip install educhain
```

## 🎮 Usage

### Generate MCQs

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1ImijJ-DF8XGTzyLJ0lq68yInrPN1-L8L?usp=sharing)

#### Quick Start

```python
from educhain import qna_engine

questions = qna_engine.generate_mcq(
    topic="Indian History",
    level="Beginner",
    num=5
)
print(questions)
```

#### Using Custom Prompt Templates

```python
from educhain import qna_engine

custom_template = """
Generate {num} multiple-choice question (MCQ) based on the given topic and level.
Provide the question, four answer options, and the correct answer.
Topic: {topic}
Learning Objective: {learning_objective}
Difficulty Level: {difficulty_level}
"""

result = qna_engine.generate_mcq(
    topic="Python Programming",
    num=2,
    learning_objective="Usage of Python classes",
    difficulty_level="Hard",
    prompt_template=custom_template,
)
print(result)
```

#### Using Different LLM Models

```python
from educhain import qna_engine
from langchain_openai import ChatOpenAI

llama3_groq = ChatOpenAI(
    model="llama3-70b-8192",
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key="GROQ_API_KEY"
)

questions = qna_engine.generate_mcq(
    topic="Chess",
    level="Hard",
    num=5,
    llm=llama3_groq
)
print(questions)
```

#### Generate Questions from Data Sources

```python
from educhain import qna_engine

questions = qna_engine.generate_mcqs_from_data(
    source="https://example.com/article",
    source_type="url",
    num=5,
    learning_objective="Understand key concepts",
    difficulty_level="Intermediate"
)
print(questions)
```

### Export Questions

```python
from educhain import to_json, to_pdf, to_csv

to_json(questions, "questions.json")  # Export questions to JSON
to_pdf(questions, "questions.pdf")    # Export questions to PDF
to_csv(questions, "questions.csv")    # Export questions to CSV
```

### Generate Lesson Plans

```python
from educhain import content_engine

topic = "Medieval History"
level = "Beginner"
lesson_plan = content_engine.generate_lesson_plan(topic, level)
print(lesson_plan)
```

## 📊 Supported Question Types

- Multiple Choice Questions (MCQ)
- Short Answer Questions
- True/False Questions
- Fill in the Blank Questions

## 🔧 Advanced Configuration

Educhain offers advanced configuration options to fine-tune its behavior. Check our [configuration guide](https://docs.educhain.ai/configuration) for more details.

## 🌟 Success Stories

Educators worldwide are using Educhain to transform their teaching. Read our [case studies](https://educhain.ai/case-studies) to learn more.

## 📈 Usage Statistics

Educhain's adoption has been growing rapidly:

<img src="/api/placeholder/600/400" alt="Usage Growth Graph" />

## 🗺 Roadmap

- [x] Bulk Generation
- [x] Outputs in JSON format
- [x] Custom Prompt Templates
- [x] Custom Response Models using Pydantic
- [x] Exports questions to JSON/PDF/CSV
- [x] Support for other LLM models
- [x] Generate questions from text/PDF file
- [ ] Finetuned Model for question generation
- [ ] Integration with popular Learning Management Systems
- [ ] Mobile app for on-the-go content generation

## 🤝 Contributing

We welcome contributions! Please see our [Contribution Guide](CONTRIBUTING.md) for more details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 📬 Contact

- For general inquiries: educhain.in
- For technical support: satvik@buildfastwithai.com
- Follow us on [Twitter](https://twitter.com/educhain_ai)

For bug reports or feature requests, please open an issue on our [GitHub repository](https://github.com/educhain/educhain).

---

<img src="images/logo.svg" alt="Educhain Logo" align="right" height = 80 width = 80 />

Made with ❤️ by Buildfastwithai

[www.educhain.in](https://educhain.in)
