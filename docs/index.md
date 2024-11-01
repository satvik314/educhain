# 🎓 Educhain Documentation

Welcome to the Educhain documentation! 🚀 Educhain is a powerful Python package that leverages Generative AI to create engaging and personalized educational content.

 <img src="logo.svg" alt="https://www.buildfastwithai.com/" height = 80 width = 80 />

## 🚀 Quick Links

| 📚 Getting Started | 🌟 Features | 🛠️ Advanced | 🤝 Community |
|:----------------:|:---------:|:----------:|:-----------:|
| [🔧 Installation](getting-started/installation.md) | [📝 MCQ Generation](features/mcq_generation.md) | [🎨 Custom Prompts](advanced-usage/custom-prompts.md) | [👥 Contributing](contributing.md) |
| [🏃‍♂️ Quick Start](getting-started/quick-start.md) | [📊 MCQ_from_data](features/mcq_from_data.md) | [🤖 LLM Models](advanced-usage/llm-models.md) | [💬 Discord](https://discord.gg/educhain) |
| [⚙️ Configuration](getting-started/configuration.md) | [📤 Export Options](features/export-options.md) | [📚 Data Sources](advanced-usage/data-sources.md) | [🌐 Website](https://educhain.in) |

## 📊 Why Educhain?



Educhain consistently outperforms traditional methods in content generation speed and quality. [Learn more about our performance](resources/case-studies.md)

## 🌟 Key Features [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]([https://colab.research.google.com/drive/1_RFeReRKFcac2SLCEjnWqLgHV2pQFgPr?usp=sharing])


- 📝 Generate Multiple Choice Questions (MCQs)  
- 📊 Create comprehensive Lesson Plans
- 🔄 Support for various LLM models
- 📁 Export questions to JSON, PDF, and CSV formats
- 🎨 Customizable prompt templates
- 📚 Generate questions from text/PDF files

## 🚀 Get Started in Minutes

```python
from educhain import Educhain

client = Educhain()

questions = client.qna_engine.generate_questions(
    topic="Indian History",
    level="Beginner",
    num=5
)
print(questions)
```

[🏃‍♂️ See our Quick Start guide for more](getting-started/quick-start.md)

## 📈 Educhain in Action

Educators worldwide are using Educhain to transform their teaching. Check out our [success stories](resources/case-studies.md) to see how Educhain is making a difference in classrooms around the globe.


## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding new features, or improving documentation, your help is appreciated.

[🤝 Learn how to contribute](contributing.md)

## 📬 Stay Connected

- 📰 [Blog](https://blog.educhain.in)
- 🐦 [Twitter](https://twitter.com/educhain_ai)
- 💼 [LinkedIn](https://www.linkedin.com/company/educhain-ai)
- 💬 [Discord Community](https://discord.gg/educhain)

## 📄 License

Educhain is open source software [licensed as MIT](https://github.com/educhain/educhain/blob/main/LICENSE).

---

<img src="logo.svg" alt="Educhain Banner" height = 80 width = 80 />

Made with ❤️ by Buildfastwithai

[www.educhain.in](https://educhain.in)
