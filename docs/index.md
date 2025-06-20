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

Educhain consistently outperforms traditional methods in content generation speed and quality. Our AI-powered platform enables educators to create high-quality learning materials in minutes instead of hours. [Learn more about our performance](resources/case-studies.md)

## 🌟 Key Features <div align="left"><a href="https://colab.research.google.com/drive/1JNjQz20SRnyRyAN9YtgCzYq4gj8iBTRH?usp=chrome_ntp#scrollTo=VY_TU5FdgQ1e" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></a></div>

### Content Generation
- 📝 Generate Multiple Choice Questions (MCQs) with explanations
- 📚 Create flashcards for effective studying
- 📊 Build comprehensive lesson plans with objectives and activities
- 📗 Generate study guides and educational summaries

### Technical Capabilities
- 🤖 Support for various LLM models (Gemini, GPT-4, Claude, etc.)
- 🌐 Multilingual content generation and preservation
- 📷 Visual question generation from images
- 📹 Content extraction from YouTube videos

### Integration & Export
- 📁 Export to multiple formats (JSON, PDF, CSV, DOCX)
- 🔗 Generate questions from URLs, PDFs, and text
- 🎨 Customizable prompt templates
- 🔥 Streamlit integration for building educational apps

## 🚀 Get Started in Minutes

```python
from educhain import Educhain

client = Educhain()
questions = client.qna_engine.generate_questions(
    topic="Indian History",
    custom_instructions="Include questions about Maharana Pratap",
    num=5
)

questions.show() 
```

[🏃‍♂️ See our Quick Start guide for more](getting-started/quick-start.md)

## 📈 Educhain in Action

Educators worldwide are using Educhain to transform their teaching. Check out our [success stories](resources/case-studies.md) to see how Educhain is making a difference in classrooms around the globe.

## 📚 Starter Apps

Explore our ready-to-use educational applications built with Educhain:

- **📚 Flashcard Generator**: Create customized flashcards on any topic with color-coded card types
- **🌍 Multilingual Chatbot**: Educational assistant that supports multiple languages
- **📝 Quiz Creator**: Generate interactive quizzes with explanations
- **📖 Lesson Planner**: Build comprehensive lesson plans with objectives and activities

Check out our [cookbook directory](/cookbook/starter-apps/) for code examples and deployment instructions.

## 💸 Roadmap  

We're constantly improving Educhain! Here's what's coming soon:  
 
- [x] **Flashcard Generation** to simplify learning  
- [x] **Multilingual Support** for global education
- [ ] **Interactive Assessment Tools** for real-time feedback
- [ ] **High-Accuracy Math Questions** with step-by-step solutions
- [ ] **Personalized Learning Paths** based on student performance
- [ ] **Try it out on our [website](https://educhain.in)** for on-the-go content creation 🚀


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
