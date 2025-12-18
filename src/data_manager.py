import json
import os

def load_quiz_file():
    directory = "data"

    quiz_files = []

    all_files = os.listdir(directory)

    for filename in all_files:
        if filename.endswith(".json"):
            quiz_files.append(filename)

    return quiz_files

def load_quiz_data(filename):
    file_path = os.path.join("data", filename)

    with open(file_path, "r") as file:
        data = json.load(file)

        return data