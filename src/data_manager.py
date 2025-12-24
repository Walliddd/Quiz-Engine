import json
import os
from src.colors import color_blue, color_cyan, color_green, color_magenta, color_red, color_yellow

def load_quiz_file():
    directory = "data"

    quiz_files = []

    ensure_data_directory("data")

    all_files = os.listdir(directory)

    for filename in all_files:
        if filename.endswith(".json"):
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
    file_path = os.path.join("data", filename)

    with open(file_path, "r") as file:
        data = json.load(file)

        return data # restituisce i dati da un file dalla lista precedente
    
def is_valid_quiz(data):

    if type(data) is not dict:
        return False
    
    if "title" not in data:
        return False
    
    if "questions" not in data:
        return False
    
    if not isinstance(data["questions"], list):
        return False
    
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
    os.makedirs(directory_name, exist_ok = True)