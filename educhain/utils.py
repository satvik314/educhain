import pandas as pd
from .models import MCQList

def to_csv(quiz_data : MCQList, file_name):
    """
    Generate a CSV file from a Quiz object.

    Args:
    quiz_data (Quiz): Instance of the Quiz class containing a list of Question objects.
    file_name (str): Name of the CSV file to be created.
    """
    mcq_data = []

    for question in quiz_data.questions:
        mcq_data.append({
            'question': question.question,
            'options': ', '.join(question.options),
            'correct_answer': question.correct_answer
        })

    df = pd.DataFrame(mcq_data)
    df.to_csv(file_name, index=False)