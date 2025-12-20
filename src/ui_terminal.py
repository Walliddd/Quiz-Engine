import os
import platform
from typing import List, Dict
import string

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

        if not selection:
            print("[WARN] Input cannot be empty. Please try again.")
            continue

        try:
            selection = int(selection_str)

            if selection >= 1 and selection <= max_option:
                return selection
            else:
                print(f"[ERROR] Your choice is out of range.")
        except ValueError:
            print(f"[ERROR] '{selection_str}' is not a valid integer. Please enter only digits.")

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

def display_question(question_data: Dict, question_number: int, total_questions: int):
    print("-" * 35)
    print(f"Question {question_number} of {total_questions} | Points {question_data.get("points", 1)}")
    print("-" * 35)

    print(f"\n{question_data["question"]}\n")

    options = question_data["options"]
    letters_uppercase = string.ascii_uppercase

    for index, option in enumerate(options):
        if index < len(letters_uppercase):
            letter = letters_uppercase[index]
            print(f"{letter}. {option}")
        else:
            print(f"[ERROR] Index '{index} out of range A-Z'")

def get_answer():
    while True:
        answer = input("Your answer (A, B, C, ...): ").strip().upper()

        if not answer:
            print("[WARN] Input cannot be empty. Please try again.")
            continue

        return answer