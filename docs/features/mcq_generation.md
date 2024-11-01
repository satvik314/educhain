## 📝 features/mcq-generation.md

```markdown
# 📝 Multiple Choice Question (MCQ) Generation

Unleash the power of AI to create engaging MCQs! 🧠✨

## 🚀 Basic Usage

```python
from educhain import Educhain

client = Educhain()
questions = client.qna_engine.generate_questions(
    topic="Python Programming",
    level="Intermediate",
    num=10
)
```

## 🎛️ Customization Options

| Option | Description | Example Values |
|--------|-------------|----------------|
| `topic` | Subject of the questions | "Machine Learning", "World History" |
| `level` | Difficulty level | "Beginner", "Intermediate", "Advanced" |
| `num` | Number of questions | 5, 10, 20 |
| `question_type` | Type of questions | "conceptual", "application", "memory" |


## 📊 Output Format

```json
[
  {
    "question": "What is a list comprehension in Python?",
    "options": [
      "A way to create lists using a for loop in one line",
      "A method to sort lists",
      "A function to compress lists",
      "A tool for list visualization"
    ],
    "correct_answer": "A way to create lists using a for loop in one line"
  },
  // More questions...
]
```

## 🌟 Pro Tips

- Use specific topics for more focused questions
- Experiment with different levels to match your audience
- Combine with our [export options](export-options.md) for easy sharing!

Ready to dive deeper? Check out our [🎨 custom prompt templates](../advanced-usage/custom-prompts.md)!
```

## 📊 features/lesson-plans.md

```markdown
# 📊 Lesson Plan Generation

Create comprehensive lesson plans with AI assistance! 📚✨

## 🚀 Basic Usage

```python
from educhain import content_engine

lesson_plan = content_engine.generate_lesson_plan(
    topic="Introduction to Photosynthesis",
    grade_level= 7,
    duration="45 minutes"
)

print(lesson_plan)
```

## 🎛️ Customization Options

| Option | Description | Example Values |
|--------|-------------|----------------|
| `topic` | Main subject of the lesson | "French Revolution", "Algebra Basics" |
| `grade_level` | 1-10 | 10-12 |
| `duration` | Length of the lesson | "30 minutes", "1 hour", "90 minutes" |
| `learning_objectives` | Specific goals for the lesson | ["Understand the process", "Identify key components"] |


## 📄 Output Format

The generated lesson plan includes:

1. Learning Objectives
2. Materials Needed
3. Introduction/Warm-up
4. Main Activities
5. Assessment/Wrap-up


## 🌟 Pro Tips

- Include specific learning objectives for more targeted plans
- Use the `teaching_style` parameter to match your preferred approach
- Combine with [MCQ generation](mcq-generation.md) for comprehensive lesson materials

Want to customize further? Explore our [🎨 custom templates](../advanced-usage/custom-prompts.md) feature!
```

## 🔢 features/question-types.md

```markdown
# 🔢 Question Types

Educhain supports various question types to diversify your assessments! 📚🧠

## 📋 Supported Question Types

1. **Multiple Choice Questions (MCQs)** 🔘
2. **True/False Questions** ✅❌
3. **Fill in the Blanks** 📝
4. **Short Answer Questions** 📄
5. **Matching Questions** 🔗

## 🚀 Usage Example

```python
from educhain import qna_engine

# Generate different types of questions
from educhain import qna_engine

questions = qna_engine.generate_questions(
    "topic": "World War II",
    "num": 2,
    "type": "Short Answer",
    "custom_instructions": "Focus on the European theater"
)
questions.show()
```

## 🎛️ Customization

Each question type supports similar customization options:

- `topic`: Subject of the questions
- `num`: Number of questions to generate
- `level`: Difficulty level (e.g., "Beginner", "Intermediate", "Advanced")


## 🌟 Pro Tips

- Mix different question types for varied assessments
- Use specific question types to target different learning objectives
- Combine with [export options](export-options.md) for easy quiz creation

Ready to create diverse question sets? Start mixing and matching question types! 🎓✨
```

## 📤 features/export-options.md

```markdown
# 📤 Export Options

Easily share and use your generated content with Educhain's export features! 💾📊

## 📋 Supported Export Formats


1. **CSV** 📑
2. **PDF** 📁
3. **JSON**


## 🚀 Usage Example

```python
from educhain import qna_engine

# Generate questions
questions = qna_engine.generate_mcq(topic="Solar System", num=5)

# Export to different formats
from educhain import to_json, to_pdf, to_csv
to_json(questions, "questions.json")  # Export questions to JSON
to_pdf(questions, "questions.pdf")    # Export questions to PDF
to_csv(questions, "questions.csv")    # Export questions to CSV
```



## 🌟 Pro Tips

- Use JSON for easy integration with other systems
- Export to PDF for print-ready quizzes
- Combine with [different question types](question-types.md) for comprehensive assessments

Ready to share your generated content? Start exporting now! 📤✨
```
