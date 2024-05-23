# educhain

A Python package for generating educational content using Generative AI. Educhain makes it easy to apply Generative AI in various educational use cases to create engaging and personalized learning experiences 

## Installation

```shell
pip install educhain
```

## Usage


### Use it to Generate MCQs

Here's an example of how to use Educhain:

## Generate MCQs

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1ImijJ-DF8XGTzyLJ0lq68yInrPN1-L8L?usp=sharing)

Here are some examples on how to use educhain: 

### Quickstart


```python
from educhain import qna_engine

questions = qna_engine.generate_mcq(
    topic="Indian History",
    level="Beginner",
    num=5
)

questions
```

### Using Custom Prompt Templates

You can create your own prompt templates and customize it with various input fields

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
    learning_objective = "Usage of Python classes",
    difficulty_level = "Hard",
    prompt_template=custom_template,
)

result
```

### Using Different LLMs

Switch from default OpenAI models to other models using ChatOpenAI.

Example shows using Llama 3 model through Groq

```python
from educhain import qna_engine
from langchain_openai import ChatOpenAI

llama3_groq = ChatOpenAI(
    model = "llama3-70b-8192",
    openai_api_base = "https://api.groq.com/openai/v1",
    openai_api_key = "GROQ_API_KEY"
)

questions = qna_engine.generate_mcq(
    topic="Chess",
    level="Hard",
    num=5,
    llm = llama3_groq
)

questions
```

### Export questions to JSON, PDF, CSV

```python

from educhain import to_json, to_pdf, to_csv

to_json(questions, "questions.json") # export questions to JSON
to_pdf(questions, "questions.pdf") # export questions to PDF
to_csv(questions, "questions.csv") # export questions to CSV

```

## Generate Lesson Plans

### Quickstart

```shell
from educhain import content_engine

topic = "Medieval History"
level = "Beginner"

lesson_plan = content_engine.generate_lesson_plan(topic, level)
print(lesson_plan)
```

## Contributing

*Contributions are welcome! Please open an issue or submit a pull request on the GitHub repository.*

## Next Steps

Will be releasing more features for MCQ Generation
- [x] Bulk Generation
- [x] Outputs in JSON format
- [x] Custom Prompt Templates
- [x] Custom Response Models using Pydantic
- [x] Exports questions to JSON/PDF/CSV
- [X] Support for other LLM models
- [ ] Generate questions from text/pdf file
- [ ] Finetuned Model for question generation



