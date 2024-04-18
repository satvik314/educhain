# educhain

A Python package for generating educational content using Generative AI. Educhain makes it easy to apply Generative AI in various educational use cases to create engaging and personalized learning experiences 

## Installation

```shell
pip install educhain
```

## Usage


### Use it to Generate MCQs

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1bseC2F00l42JPVN2-35fwMupeTnyYGME?usp=sharing)

Here's an example of how to use EduChain:

```python
from educhain import generate_mcq, to_csv, to_json, to_pdf, generate_mcq_from_pdf
```

### Generate multiple-choice questions with given number of questions

```python
mcq = generate_mcq(topic="Python", level="Advanced", num=5, custom_template="All questions should be word problems")
print(mcq)
```

#### Save the MCQ to a CSV file

```python
to_csv(mcq, "mcq.csv")
```

#### Save the MCQ to a JSON file
```python
to_json(mcq, "mcq.json")
```

#### Save the MCQ to a PDF file

- **heading** (str): (optional)
- **subheading** (str): (optional)

```python
to_pdf(mcq, "mcq.pdf", heading="Python MCQ", subheading="Advanced Level - (10 Questions)")
```

### Generate multiple-choice questions with given pdf file

```python
mcq = generate_mcq_from_pdf("ai_intro.pdf", num=5)
```

### Effortlessly create Lesson Plans

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
- [x] Export questions to CSV
- [x] Exports questions to JSON
- [x] Exports questions to PDF
- [ ] Support for other LLM models
- [ ] Generate questions from text/pdf file
- [ ] Finetuned Model for question generation



