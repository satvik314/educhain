# educhain

A Python package for generating educational content using Generative AI. Educhain makes it easy to apply Generative AI in various educational use cases to create engaging and personalized learning experiences 

## Installation

```shell
pip install git+https://github.com/satvik314/educhain.git
```

## Usage

### Use it to Generate MCQs

##### Default : (no. of ques: 1, no csv generated)

```shell
from educhain import qna_engine

topic = "Quantum Entanglement"
level = "Intermediate"

mcq = qna_engine.generate_mcq(topic, level)
print(mcq)
```

##### With given no. of ques, no csv generated

```shell
from educhain import qna_engine

topic = "Quantum Entanglement"
level = "Intermediate"
num = 5

mcq = qna_engine.generate_mcq(topic, level, num)
print(mcq)
```
##### With given no. of ques. & csv generated with given file_name

```shell
from educhain import qna_engine

topic = "Quantum Entanglement"
level = "Intermediate"
num = 5
file_name="python_mcq.csv"

mcq = qna_engine.generate_mcq(topic, level, num, file_name)
print(mcq)
```

### Effortlessly create Lesson Plans


```shell
from educhain import content_engine

topic = "Medieval History"
level = "Beginner"

lesson_plan = content_engine.generate_lesson_plan(topic, level)
print(lesson_plan)
```


## Next Steps

Will be releasing more features for MCQ Generation
- Bulk Generation
- Outputs in JSON format
- Export questions to CSV
- Generate questions from text/pdf file
- Finetuned Model for question generation



