import json
from pathlib import Path
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

    saved_path = save_quiz_to_file(new_quiz_data)

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
                collect_question_details(quiz_data)
                break
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

    new_id = len(quiz_data["questions"])

    while True:
        question = get_validated_text(prompt="Insert the Question: ", error_msg="Question cannot be empty.")

        category = get_validated_text(prompt="Insert the Category name: ", error_msg="Category cannot be empty.")

        option_list = collect_options_with_limit()

        correct_index = collect_and_validate_index(option_number = len(option_list))

        explanation = get_validated_text("Insert the Answer Explanation: ")

        points = collect_and_validate_int("Points to be assigned (e.g. 10): ")

        penalty = collect_and_validate_int("Penalty in case of Error (e.g. 2): ")
            
        time_limit = collect_and_validate_int("Time limit in seconds (e.g. 30): ")

        new_question = {
            "id": new_id,
            "question": question,
            "category": category,
            "options": option_list,
            "correct_index": correct_index,
            "explanation": explanation,
            "points": points,
            "penalty": penalty,
            "time_limit": time_limit
        }

    quiz_data["questions"].append(new_question)

    print(color_green(f"\nQuestion added with success."))
          
def get_validated_text(prompt, error_msg):
    while True:
        user_input = input(prompt)

        if user_input.strip() == "":
            print(color_red(f"[ERROR] {error_msg}"))
            continue
        else:
            return user_input.strip()

def collect_options_with_limit():
    max_options = 5
    min_options = 2

    options = []

    while True:
        if len(options) >= max_options:
            print(color_yellow(f"\nYou reached the max limit of {max_options} Options."))
            break

        prompt = f"Insert the Option #{len(options) + 1}: "
        new_option = get_validated_text(prompt, "The option cannot be empty.")
        options.append(new_option)

        if len(options) >= min_options:
            add_more = input("Do you want to add another option? (y/n): ").strip().lower()
            if add_more == "n":
                break
        
    if len(options) < min_options:
        print(color_red(f"[ERROR] At least {min_options} are required."))
        return collect_options_with_limit()
    
    return options

def collect_and_validate_index(option_number):
    print(color_blue(f"The input must be between 1 and {option_number}."))

    while True:
        input_str = input(f"Insert the index of the correct answer (e.g. 1, 2, ...): ")

        try:
            user_choice_base1 = int(input_str)
        except ValueError:
            print(color_red(f"Invalid input. Enter an integer."))
            continue

        python_index = user_choice_base1 - 1

        if 0 <= python_index < option_number:
            print(color_green(f"[SUCCESS] The converted index is valid."))

            return python_index
        
        else:
            print(color_red("[ERROR] The number is an integer, but it's out of options range"))
            continue

def collect_and_validate_int(prompt, error_msg, allow_zero):
    while True:
        input_str = input(prompt)

        try:
            value = int(input_str)
        except ValueError:
            print(color_red("[ERROR] You must insert a valid integer number."))
            continue

        if allow_zero == False:
            if value <= 0:
                print(color_red(f"[ERROR] The value must be strictly positive (>0)."))
                continue

        return value
    
def collect_and_validate_index(option_number):
    instructions = f"The correct answer is one of {option_number} options. Insert the number (1 to {option_number}): "

    while True:
        input_str = input(instructions)

        try:
            choice_base1 = int(input_str)
        except ValueError:
            print(color_red("[ERROR] Invalid input. Insert integers only."))
            continue

        python_index = choice_base1 - 1

        if 0 <= python_index < option_number:
            print(color_green(f"[SUCCESS] Correct index registered."))

            return python_index
        else:
            print(color_red(f"Choice out of range. It must be between 1 and {option_number}"))
            continue

def sanitize_title_for_filename(title):
    sanitized = title.lower()

    sanitized = sanitized.replace(" ", "-")

    prohibited_chars = ["/", "\\", ":", "*", "?", "\"", "<", ">", "|"]

    for char in prohibited_chars:
        sanitized = sanitized.replace(char, "")

    sanitized = sanitized.replace("--", "-")

    sanitized = sanitized.strip("-")

    filename = sanitized + ".json"

    return filename

def save_quiz_to_file(quiz_data):
    title = quiz_data.get("title", "untitled_quiz")

    filename = sanitize_title_for_filename(title)

    file_path = Path("data") / filename

    try: 
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, indent=4)

        print(color_green(f"\n[SUCCESS] Quiz saved to: {file_path}"))

        return str(file_path)
    except IOError as e:
        print(color_red(f"\n[CRITICAL ERROR] Could not save file {file_path}."))
        print(f"\nDetails: {e}")

        return None