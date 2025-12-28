import os
import platform
from typing import List, Dict
import string
from src.colors import color_red, color_yellow, color_blue, color_cyan

def print_welcome():
    """
    this function prints a welcome message to the user when they start
    (the function body is currently empty, just using 'pass')
    """
    pass


def show_menu(quiz_list):
    """
    this function show the list of available quizzes with their IDs and the option to create a new one

    args:
        quiz_list(list[dict]):  a list of dictionaries. each dictionary represents one quiz and must have
                                the keys "id" and "title"
        
    returns:
        int: the highest numerical ID available for selecting an existing quiz
    """
    for quiz in quiz_list:
        print(f"[{quiz["id"]}] {quiz["title"]}")
    
    max_quiz_id = len(quiz_list)
    print(f"[C] Create New Quiz")

    return max_quiz_id

def get_user_choice(max_option):
    """
    this function asks the user to select an existing quiz (using a number ID) or to create a new quiz (C)

    it checks the input very carefully, making sure it is a valid whole number between 1 and the maximum
    option number, or the letter 'C' 

    args:
        max_option (int ): the highest number of quizzes available to choose from

    returns:
        int or str:   the number ID of the selected quiz(int), or the string 'c' if the user chooses to create a quiz
    """
    while True:
        clear_screen()
        print_header()

        selection_str = input(f"\nSelect a quiz (1 - {max_option}): ").strip()

        if not selection_str:
            warn = color_yellow("[WARN]")
            message = "Input cannot be empty. Please try again."
            print(f"{warn} {message}")
            continue

        if selection_str.upper() == "C":
            return "C"

        try:
            selection = int(selection_str)

            if selection >= 1 and selection <= max_option:
                return selection
            else:
                message = "Your choice is out of range."
                error = color_red("[ERROR]")
                print(f"{error} {message}")
        except ValueError:
            message = f"'{selection_str}' is not a valid integer. Please enter only digits."
            error = color_red("[ERROR]")
            print(f"{error} {message}")

def clear_screen():
    """
    this function cleans up the console based on the detected operating system
    """
    if platform.system() == "Windows":
        os.system("cls")

    else:
        os.system("clear")

def print_header(): # ascii art font name: 'Classy'
    """
    this function prints the ascii art with the logo of the program
    """
    header = """
                                                                  
   ▄▄▄▄                         ▄▄▄▄▄▄▄                           
 ▄█▀▀███▄▄                     █▀██▀▀▀                            
 ██    ██       ▀▀               ██     ▄        ▄▄ ▀▀ ▄          
 ██    ██ ██ ██ ██ ▀▀▀██         ████   ████▄ ▄████ ██ ████▄ ▄█▀█▄
 ██  ▄ ██ ██ ██ ██   ▄█▀ ▀▀▀▀    ██     ██ ██ ██ ██ ██ ██ ██ ██▄█▀
  ▀█████▄▄▀██▀█▄██▄▄██▄▄         ▀█████▄██ ▀█▄▀████▄██▄██ ▀█▄▀█▄▄▄
       ▀█                                        ██               
                                               ▀▀▀                """
    print(color_cyan(header))

def display_question(question_data: Dict, question_number: int, total_questions: int):
    """
    this function shows the question text, the points it gives, 
    and the answer options formatted with capital letters (A, B, C...)

    args:
        question_data (dict): a dictionary containing the question details
        question_number (int): the step by step number of the questions being shown
        total_questions (int): the total number of questions in the quiz
    """
    print(color_blue("-") * 35)
    print(f"Question {question_number} of {total_questions} | Points {question_data.get("points", 1)}")
    print(color_blue("-") * 35)

    print(f"\n{question_data["question"]}\n")

    options = question_data["options"]
    letters_uppercase = string.ascii_uppercase

    for index, option in enumerate(options):
        if index < len(letters_uppercase):
            letter = letters_uppercase[index]
            print(f"{letter}. {option}")
        else:
            message = f"Index '{index}' out of range A-Z"
            error = color_red("[ERROR]")
            print(f"{error} {message}")

def get_answer():
    """
    this function asks the user for an answer using a capital letter

    it keeps asking until the user types something that is not empty

    returns:
        str: the user's answer in capital letters
    """
    while True:
        answer = input("Your answer (A, B, C, ...): ").strip().upper()

        if not answer:
            print("[WARN] Input cannot be empty. Please try again.")
            continue

        return answer
    
def get_username():
    """
    this function asks the user to enter their username

    it shows the welcome screen/header before asking for the name

    returns:
        str: the username provided by the user
    """
    while True:
        clear_screen()
        print_header()

        username = input(f"Insert your Username: ")

        if not username:
            warn = color_yellow("[WARN]")
            message = "Input cannot be empty. Please try again."
            print("{warn} {message}")
            continue

        return username
    
def print_top_10(top_10_list):
    """
    this function shows the first 10 leaderboards results
    the text is centered and formatted nicely

    args:
        top_10_list (list[dict]):   a list containing the top 10 score records, already sorted from
                                    highest score to lowest
    """
    clear_screen()
    print_header()

    if not top_10_list:
        print(f"No results found on the Leaderboard.")
        return
    
    print(color_blue(f"\n--- LEADERBOARD TOP 10 FOR {top_10_list[0]["quiz_name"].upper()} ---"))

    for index, record in enumerate(top_10_list):
        print(f"\n{index + 1} - {record["username"]} - {record["quiz_name"]} - {record["score"]} - {record["date"]}")