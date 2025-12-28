import json
import os
from src.colors import color_blue, color_cyan, color_green, color_magenta, color_red, color_yellow

def load_quiz_file():
    """
    this function looks inside the 'data' folder and gives back a list of names for the JSON files that 
    are valid quizzes 

    first it makes sure the 'data' folder exists. if a JSON file is not correct (eiter the structure is bad),
    the function skips it and prints a helpful message

    returns:
        list[str]: a list of strings with the names of the valid JSON files found (example: ["quiz1.json", "quiz2.json"]) 
    """
    directory = "data"

    quiz_files = []

    ensure_data_directory("data")

    all_files = os.listdir(directory)

    for filename in all_files:
        if filename.endswith(".json"):
            if filename == "leaderboard.json":
                continue

            data = load_quiz_data(filename)
            is_valid = is_valid_quiz(data)
            
            if is_valid:
                quiz_files.append(filename)
            else:
                info = color_cyan("[INFO]")
                message = f"Skipping invalid quiz file: {filename}"
                print(f"{info} {message}")

    return quiz_files # restituisce i file json (in una lista) nella cartella dati

def load_quiz_data(filename):
    """
    this function loads the JSON content from a specific file in the 'data' folder

    args:
        filename (str): the name of the JSON file to load (it must be in 'data/')
    
    returns:
        dict: the content of the JSON file loaded as a python dictionary
    """
    file_path = os.path.join("data", filename)

    with open(file_path, "r") as file:
        data = json.load(file)

        return data # restituisce i dati da un file dalla lista precedente
    
def is_valid_quiz(data):

    """
    this function checks if the structure of the loaded dictionary matches what is expected for a quiz

    it checks:
    - that the data is actually a dictionary
    - that it has the key 'title' (which must be a text string) and 'questions' (which must be a list)
    - that every item in the "questions" list is a dictionary with the basic structure (it must have 'question', 'options', and 'correctOption')
    - that 'options' is a list with at least 2 items 
    - that 'correctOption' is a valid index number for the options' list

    args:
        data(any): the data loaded ffrom the JSON file
    
    returns:
        bool: true if the structure is correct, false if it is not
    """

    if type(data) is not dict:
        return False
    
    if "title" not in data:
        return False
    
    if "questions" not in data:
        return False
    
    if not isinstance(data["questions"], list):
        return False
    
    # check for every single question
    for question in data["questions"]:
        if not isinstance(question, dict):
            return False
            
        if "question" not in question:
            return False

        if not isinstance(question["question"], str):
            return False

        if "options" not in question:
            return False

        if not isinstance(question["options"], list):
            return False
        
        if not (len(question["options"]) >= 2):
            return False
        
        if "correctOption" not in question:
            return False
        
        if not isinstance(question["correctOption"], int):
            return False
        
        if not (0 <= question["correctOption"] < len(question["options"])):
            return False
    
    return True

def ensure_data_directory(directory_name):
    """
    this function checks if a given folder exists and creates it if it is missing

    args:
        directory_name (str): the name of the folder to check/create (example: "data")
    """

    os.makedirs(directory_name, exist_ok = True)