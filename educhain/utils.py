import pandas as pd

def to_csv(data, file_name, num):
    """
    Generate CSV file with given data.

    Args:
    filename (str): Name of the CSV file.
    data (json): Data to be written to the CSV file.
    """
    
    # Create a DataFrame from the JSON data
    mcq_data = []
    
    if (num > 1):    
        for mcq in data["questions"]:
            mcq_data.append({
                'question': mcq["question"],
                'options': ', '.join(mcq["options"]),
                'answer': mcq["correct_answer"],
            })
    else:
        mcq_data.append({
            'question': data["question"],
            'options': ', '.join(data["options"]),
            'answer': data["correct_answer"],
        })

    df = pd.DataFrame(mcq_data)

    # Save the DataFrame to a CSV file
    df.to_csv(file_name, index=False)