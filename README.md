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
![do_it](https://github.com/lunatic-7/educhain/assets/90578650/611c5c24-47b6-413f-92e9-ab97e41c0f4d)

### Generate a multiple-choice question with given number of questions


```python
from educhain import generate_mcq, to_csv, to_json, to_pdf
```![do_it](https://github.com/lunatic-7/educhain/assets/90578650/99d3aa0d-c7cc-4b42-880d-fa7996544e98)

### **generate_mcq** function

The generate_mcq function takes the following arguments:
- **topic** (str): The topic for which you want to generate MCQs.
- **level** (str): The difficulty level of the MCQs (e.g., "Beginner", "Intermediate", "Advanced").
- **num** (int, optional): The number of MCQs to generate. Defaults to 1.
- **llm** (LLM, optional): An instance of a language model from the langchain library. If not provided, the function will use the ChatOpenAI model with the "gpt-3.5-turbo-0125" version.

The function returns an instance of the MCQList class, which is a custom class defined in the library. It contains a list of Question objects, each representing a single MCQ.

```python
mcq = generate_mcq(topic="Python", level="Advanced", num=5)
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

- **heading** (str) (optional)
- **subheading** (str) (optional)

```python
to_pdf(mcq, "mcq.pdf", heading="Python MCQ", subheading="Advanced Level - (10 Questions)")
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



