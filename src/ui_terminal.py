import os
import platform
from typing import List, Dict
import string
from src.colors import color_red, color_green, color_yellow, color_blue, color_cyan, color_magenta

def print_welcome():
    pass

def show_menu(quiz_list):
    for quiz in quiz_list:
        print(f"[{quiz["id"]}] {quiz["title"]}")

def get_user_choice(max_option):
    while True:
        clear_screen()
        print_header()

        selection_str = input(f"\nSelect a quiz (1 - {max_option}): ").strip()

        if not selection_str:
            warn = color_yellow("[WARN]")
            message = "Input cannot be empty. Please try again."
            print(f"{warn} {message}")
            continue

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
    if platform.system() == "Windows":
        os.system("cls")

    else:
        os.system("clear")

def print_header():
    header = """ # ascii art font name: 'Classy'
                                                                  
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
    while True:
        answer = input("Your answer (A, B, C, ...): ").strip().upper()

        if not answer:
            print("[WARN] Input cannot be empty. Please try again.")
            continue

        return answer
    
def get_username():
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
    clear_screen()
    print_header()

    if not top_10_list:
        print(f"No results found on the Leaderboard.")
        return
    
    print(color_blue(f"\n--- LEADERBOARD TOP 10 FOR {top_10_list[0]["quiz_name"]} ---"))

    for index, record in enumerate(top_10_list):
        print(f"\n{index + 1} - {record["username"]} - {record["quiz_name"]} - {record["score"]} - {record["date"]}")