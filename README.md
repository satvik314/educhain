<p align="center">
  <img src="https://github.com/VedantDeshmukh2/educhain/blob/main/images/educhain.svg" alt="Educhain Logo" width="800" height="400">
</p>


<div align="center">
  
  [![PyPI version](https://badge.fury.io/py/educhain.svg)](https://badge.fury.io/py/educhain)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python Versions](https://img.shields.io/pypi/pyversions/educhain.svg)](https://pypi.org/project/educhain/)
  [![Downloads](https://pepy.tech/badge/educhain)](https://pepy.tech/project/educhain)

</div>

# Educhain 🎓🔗
[Website](https://educhain.in) | [Documentation](docs/index.md) 

Educhain is a powerful Python package that leverages Generative AI to create engaging and personalized educational content. From generating multiple-choice questions to crafting comprehensive lesson plans, Educhain makes it easy to apply AI in various educational scenarios.

<img src="images/logo.svg" alt="Educhain Logo" align="center" height = 120 width = 120 />

## 🚀 Features

- 📝 Generate Multiple Choice Questions (MCQs)
- 📊 Create Lesson Plans
- 🔄 Support for various LLM models
- 📁 Export questions to JSON, PDF, and CSV formats
- 🎨 Customizable prompt templates
- 📚 Generate questions from text/PDF/URL files
- 📹 Generate questions from youtube videos
- 🥽 Generate questions from images


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
from educhain import Educhain

client = Educhain()

ques = client.qna_engine.generate_questions(topic="Newton's Law of Motion",
                                            num=5,
                                            custom_instructions = "Give me some basic questions")
print(ques)
ques.json() # ques.dict()
```

#### Support Different Question Types

```python
# Supports "Multiple Choice" (default); "True/False"; "Fill in the Blank"; "Short Answer"

from educhain import Educhain

client = Educhain()

ques = client.qna_engine.generate_questions(topic = "Psychology", 
                                            num = 10,
                                            question_type="Fill in the Blank")

print(ques)
ques.json() #ques.dict()
```


#### Using Custom Prompt Templates

```python
from educhain import Educhain

client = Educhain()

custom_template = """
Generate {num} multiple-choice question (MCQ) based on the given topic and level.
Provide the question, four answer options, and the correct answer.
Topic: {topic}
Learning Objective: {learning_objective}
Difficulty Level: {difficulty_level}
"""

ques = client.qna_engine.generate_questions(
    topic="Python Programming",
    num=2,
    learning_objective="Usage of Python classes",
    difficulty_level="Hard",
    prompt_template=custom_template,
)

print(ques)
```

#### Using Different LLM Models

```python
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI

gemini_flash = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-exp-0827",
    google_api_key="GOOGLE_API_KEY")

flash_config = LLMConfig(custom_model=gemini_flash)

client = Educhain(flash_config) #using gemini model with educhain

ques = client.qna_engine.generate_questions(topic="Psychology",
                                            num=10)

print(ques)
ques.json() #ques.dict()
```

#### Generate Questions from Data Sources (URL/PDF/Text)

```python
from educhain import Educhain
client = Educhain()

ques = client.qna_engine.generate_questions_from_data(
    source="https://en.wikipedia.org/wiki/Big_Mac_Index",
    source_type="url",
    num=5)

print(ques)
ques.json() # ques.dict()
```

### Generate Lesson Plans

```python
from educhain import Educhain

client = Educhain()

plan = client.content_engine.generate_lesson_plan(
                              topic = "Newton's Law of Motion")

print(plan)
plan.json()  # plan.dict()
```

## 📊 Supported Question Types

- Multiple Choice Questions (MCQ)
- Short Answer Questions
- True/False Questions
- Fill in the Blank Questions

## 🔧 Advanced Configuration

Educhain offers advanced configuration options to fine-tune its behavior. Check our [configuration guide](https://docs.educhain.ai/configuration) for more details.


## 📈 Usage Statistics

Educhain's adoption has been growing rapidly:

<img src="/api/placeholder/600/400" alt="Usage Growth Graph" />

## 🗺 Roadmap

- [x] Bulk Generation
- [x] Outputs in JSON format
- [x] Custom Prompt Templates
- [x] Custom Response Models using Pydantic
- [x] Support for other LLM models
- [x] Generate questions from text/PDF file
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
