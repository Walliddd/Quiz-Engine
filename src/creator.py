import json
import pathlib
from src.colors import color_red, color_green, color_yellow, color_blue
from src.ui_terminal import clear_screen, print_header
from src.data_manager import ensure_data_directory

difficulty_map = {
    1: "Easy",
    2: "Medium",
    3: "Hard"
}

def run_quiz_creator():
    clear_screen()
    print_header()
    print(color_blue("\n-") + color_blue("-") *34)
    print(color_green(f"Welcome into the Quiz Creator CLI!"))
    print(color_blue("-" * 35))

    while True:
        title = input("\nWhat's the Title of the Quiz? ")

        if not title.strip():
            print(f"\nYou can't leave the title blank. Please, try again.")
            continue
        else:
            break

    while True:
        print(f"\nWhat's the Difficulty of your Quiz?")
        print(f"1. Easy")
        print(f"2. Medium")
        print(f"3. Hard")

        difficulty_str = input("\nSelect the Difficulty Level: ")

        try:
            difficulty = int(difficulty_str)
            if difficulty >= 1 and difficulty <= 3:
                break
            else:
                message = "Your choice is out of range."
                error = color_red("[ERROR]")
                print(f"{error} {message}")
        except ValueError as v:
            error = color_red("[ERROR]")
            message = "'{difficulty_str}' is not a valid integer. Please enter only digits."
            print(f"{error} {message}")
            continue

    ensure_data_directory("data")
    
    final_difficulty = difficulty_map[difficulty]

    new_quiz_data = {
        "title": title.strip(),
        "difficulty": final_difficulty,
        "questions": []
        }
    
    quiz_complete = add_questions(new_quiz_data)

    return new_quiz_data

def add_questions(quiz_data):
    while True:
        while True:
            print(color_blue("\n-") + color_blue("-") *34)
            print(color_green(f"Do you want to add Questions to your Quiz?"))
            print(color_blue("-" * 35))

            selection = input("Insert your answer (y/n): ").strip().lower()

            if selection == "n":
                break
            if selection == "y":
                print("Okay, let's proceed with adding a question...")
                collect_question_details
            else:
                message = "Invalid input"
                error = color_red("[ERROR]")
                print(f"{error} {message}")
                continue
        
        if len(quiz_data["questions"]) == 0:
            print(f"\nYou must insert at least one Question.")
            continue
        else:
            break

def collect_question_details(quiz_data):
    while True:
        question = input("Insert the Question: ")

        if not question:
            continue