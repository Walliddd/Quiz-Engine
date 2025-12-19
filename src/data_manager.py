import json
import os

def load_quiz_file():
    directory = "data"

    quiz_files = []

    all_files = os.listdir(directory)

    for filename in all_files:
        if filename.endswith(".json"):
            quiz_files.append(filename)

    return quiz_files # restituisce i file json (in una lista) nella cartella dati

def load_quiz_data(filename):
    file_path = os.path.join("data", filename)

    with open(file_path, "r") as file:
        data = json.load(file)

        return data # restituisce i dati da un file dalla lista precedente
    
def is_valid_quiz(data):

    quiz_is_valid = False

    if type(data) is dict:
        if "title" in data:

            if "questions" in data:
                if isinstance(data["questions"], list):

                    for question in data["questions"]:

                        if type(question) is dict:

                            if "question" in question:
                                if isinstance(question["question"], str):

                                    if "options" in question:
                                        if isinstance(question["options"], list) and len(question["options"])>=2:

                                            if "correctOption" in question and (question["correctOption"] >= 0 and question["correctOption"] <= len(question["options"])):
                                                if isinstance(question["correctOption"], int):
                                                    quiz_is_valid = True
                                                else:
                                                    quiz_is_valid = False
                                                    
    return quiz_is_valid