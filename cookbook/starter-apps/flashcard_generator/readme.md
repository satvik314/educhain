# 📚 Educhain Flashcard Generator

A powerful AI-powered flashcard generator built with Streamlit and the Educhain library. Create customized flashcards on any topic to enhance your learning experience.

![Flashcard Generator Demo](https://github.com/satvik314/educhain/raw/main/images/flashcard_demo.png)

## ✨ Features

- 🤖 Powered by OpenAI's GPT models through the Educhain library
- 🎯 Generate flashcards on any topic with a single click
- 🏷️ Color-coded card types (Concept, Definition, Fact, Process, Example, Comparison)
- 📝 Detailed explanations for each flashcard
- 🔢 Customize the number of flashcards generated
- 🔑 Bring your own OpenAI API key

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- An OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/satvik314/educhain.git
   cd educhain/cookbook/starter-apps/flashcard_generator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## 🔧 Usage

1. Enter your OpenAI API key in the sidebar
2. Type a topic for your flashcards (e.g., "Python Programming", "Machine Learning", "World History")
3. Select the number of flashcards you want to generate (1-20)
4. Click "Generate Flashcards"
5. Explore your flashcards by clicking on each expandable card

## 🧩 Card Types

The flashcard generator creates different types of cards to enhance your learning:

- **Concept** (Red): Core ideas and principles
- **Definition** (Teal): Precise meanings of terms
- **Fact** (Yellow): Specific pieces of information
- **Process** (Purple): Step-by-step procedures
- **Example** (Green): Practical instances or applications
- **Comparison** (Blue): Contrasting related concepts

## 🛠️ Customization

You can customize the app by modifying the following:

- Change the model used by updating the `model_name` parameter in the `LLMConfig` class
- Adjust the maximum number of flashcards by changing the `max_value` parameter in the number input
- Modify the prompt template to generate different types of content

## 📄 License

This project is part of the Educhain library and is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Educhain GitHub Repository](https://github.com/satvik314/educhain)
- [Educhain Documentation](https://github.com/satvik314/educhain/blob/main/README.md)

---

Built with ❤️ using [Educhain](https://github.com/satvik314/educhain) and [Streamlit](https://streamlit.io)