# Experiments

This file records all the experiments and features added to the project.

## Experiment 1: Generate CBSE Question Paper (maths) (Date: 18-8-2024)

* Description: Initial setup of the project to generate CBSE question papers on the fly.
* Features:
        + Added functionality to generate question papers for Mathematics subject.
        + Implemented support for Class XII.
        + Used the ```pylatexenc``` to handle latex.
  







## Experiment 2: Adaptive Quiz Class (Date: 24-8-2024)

* Description: Created the adaptive quiz class for adaptive question answering
* Features:
  
- **`db`** (`str`): Specifies the database to be used. Default is `None`. If `"supabase"` is provided, a connection to Supabase will be initialized.
  
- **`llm`** (`object`): The language model (LLM) used for generating questions. If not provided, the class will automatically initialize an LLM.
  
- **`difficulty_increase_threshold`** (`str`): The threshold for increasing the difficulty of questions. Default is `"Medium"`.
  
- **`topic`** (`str`): The topic of the quiz. Default is an empty string (`""`).
  
- **`num_questions`** (`int`): The number of questions to generate in the quiz. Default is `5`.
  
- **`custom_instruction`** (`str`): Custom instructions for generating the quiz questions. Default is an empty string (`""`).
  
- **`show_options`** (`bool`): A boolean indicating whether to immediately show answer options to the user. Default is `False`.
  
- **`data`** (`any`): External data that might influence question generation. Default is `None`.
  
- **`source_type`** (`str`): Specifies the source type for quiz data. Default is `None`.


## Experiment 3: Integration with Latex (Date: YYYY-MM-DD)

* Description: Integrated Latex support to render mathematical equations in the question paper.
* Features:
        + Added Latex rendering for mathematical equations.
        + Improved formatting of question papers.

## Experiment 4: Markdown Support (Date: YYYY-MM-DD)

* Description: Added support for Markdown formatting in the question paper generator.
* Features:
        + Implemented Markdown rendering for question papers.
        + Improved readability of question papers.
