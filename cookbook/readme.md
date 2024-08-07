# Educhain Cookbook

Welcome to the Educhain Cookbook! This cookbook provides a guide on how to utilize the functionalities of the Educhain Python package for generating educational content using Generative AI. Whether you're an educator looking to create personalized learning experiences or a developer interested in leveraging Generative AI for educational purposes, Educhain makes it easy and efficient.

## Table of Contents

1. [Installation](#installation)
2. [Generating Multiple Choice Questions (MCQs)](#generating-mcqs)
3. [Creating Lesson Plans](#creating-lesson-plans)

## 1. Installation <a name="installation"></a>

To get started with Educhain, you need to install the package via pip. Run the following command in your terminal:

```bash
pip install git+https://github.com/satvik314/educhain.git
```

## 2. Generating Multiple Choice Questions (MCQs) <a name="generating-mcqs"></a>

#### Default Usage

You can use Educhain to generate MCQs effortlessly..

```python
from educhain import qna_engine

topic = "Quantum Entanglement"
level = "Intermediate"

mcq = qna_engine.generate_mcq(topic, level)
print(mcq)
```

#### Generating Multiple Questions

If you need multiple MCQs

```python
from educhain import qna_engine

topic = "Quantum Entanglement"
level = "Intermediate"
num = 5

mcq = qna_engine.generate_mcq(topic, level, num=num)
print(mcq)
```

This will generate 5 MCQs on the topic of Quantum Entanglement.

## 3. Creating Lesson Plans <a name="creating-lesson-plans"></a>

Educhain also allows you to effortlessly create lesson plans tailored to your specified topic and level.

```python
from educhain import content_engine

topic = "Medieval History"
level = "Beginner"

lesson_plan = content_engine.generate_lesson_plan(topic, level)
print(lesson_plan)
```

This will generate a lesson plan suitable for beginners on the topic of Medieval History.

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

### Conclusion

Educhain simplifies the process of generating educational content using Generative AI. With its intuitive functions, educators and developers can create engaging and personalized learning experiences tailored to various topics and levels. Explore the possibilities with Educhain and enhance your educational materials today!
