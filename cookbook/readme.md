# Educhain Cookbook

Welcome to the Educhain Cookbook! This cookbook provides a guide on how to utilize the functionalities of the Educhain Python package for generating educational content using Generative AI. Whether you're an educator looking to create personalized learning experiences or a developer interested in leveraging Generative AI for educational purposes, Educhain makes it easy and efficient.

## Table of Contents

1. [Installation](#installation)
2. [Generating Multiple Choice Questions (MCQs)](#generating-mcqs)
3. [Save the MCQ to CSV file](#saving-csv)
4. [Save the MCQ to JSON file](#saving-json)
5. [Save the MCQ to PDF file](#saving-pdf)
6. [Creating Lesson Plans](#creating-lesson-plans)

## 1. Installation <a name="installation"></a>

To get started with Educhain, you need to install the package via pip. Run the following command in your terminal:

```bash
pip install git+https://github.com/satvik314/educhain.git
```

## 2. Generating Multiple Choice Questions (MCQs) <a name="generating-mcqs"></a>

#### Default Usage

You can use Educhain to generate MCQs effortlessly..

##### **generate_mcq** function

The generate_mcq function takes the following arguments:
- **topic** (str): The topic for which you want to generate MCQs.
- **level** (str): The difficulty level of the MCQs (e.g., "Beginner", "Intermediate", "Advanced").
- **num** (int, optional): The number of MCQs to generate. Defaults to 1.
- **llm** (LLM, optional): An instance of a language model from the langchain library. If not provided, the function will use the ChatOpenAI model with the "gpt-3.5-turbo-0125" version.
- **topic** (str): The topic for which you want to generate MCQs.
- **level** (str): The difficulty level of the MCQs (e.g., "Beginner", "Intermediate", "Advanced").
- **num** (int, optional): The number of MCQs to generate. Defaults to 1.
- **llm** (LLM, optional): An instance of a language model from the langchain library. If not provided, the function will use the ChatOpenAI model with the "gpt-3.5-turbo-0125" version.

The function returns an instance of the MCQList class, which is a custom class defined in the library. It contains a list of Question objects, each representing a single MCQ.

```python
from educhain import qna_engine, to_csv, to_json, to_pdf

topic = "Quantum Entanglement"
level = "Intermediate"
num = 5

mcq = qna_engine.generate_mcq(topic, level, num=num)
print(mcq)
```

### 3. Save the MCQ to a CSV file  <a name="saving-csv"></a>

```python
to_csv(mcq, "mcq.csv")
```

### 4. Save the MCQ to a JSON file <a name="saving-json"></a>
```python
to_json(mcq, "mcq.json")
```

### 5. Save the MCQ to a PDF file <a name="saving-pdf"></a>

- **heading** (str): (optional)
- **subheading** (str): (optional)

```python
to_pdf(mcq, "mcq.pdf", heading="Quantum Entanglement MCQ", subheading="Intermediate Level - (5 Questions)")
```

This will generate 5 MCQs on the topic of Quantum Entanglement.

## 6. Creating Lesson Plans <a name="creating-lesson-plans"></a>

Educhain also allows you to effortlessly create lesson plans tailored to your specified topic and level.

```python
from educhain import content_engine

topic = "Medieval History"
level = "Beginner"

lesson_plan = content_engine.generate_lesson_plan(topic, level)
print(lesson_plan)
```

This will generate a lesson plan suitable for beginners on the topic of Medieval History.

### Conclusion

Educhain simplifies the process of generating educational content using Generative AI. With its intuitive functions, educators and developers can create engaging and personalized learning experiences tailored to various topics and levels. Explore the possibilities with Educhain and enhance your educational materials today!
