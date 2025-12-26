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
    """
    start the interactive process to make a new quiz using the command line interface

    the function helps the user collect the following informations:
        1. quiz title (it cannot be empty)
        2. difficulty (easy, medium, hard)
        3. questions, options, correct answers, and related details (points, time limit)

    after creating the questions, show a summary and ask if the user wants to save it

    returns:
    dict or None:   a dictionary with all the quiz data if saving is confirmed and works well.
                    it returns None if the user chooses to not to save the quiz
    """
    clear_screen()
    print_header()
    print(color_blue("\n-") + color_blue("-") *34)
    print(color_green(f"Welcome into the Quiz Creator CLI!"))
    print(color_blue("-" * 35))

    # title collection
    while True:
        title = input("\nWhat's the Title of the Quiz? ")

        if not title.strip():
            print(f"\nYou can't leave the title blank. Please, try again.")
            continue
        else:
            break
    
    # difficulty collection
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
    
    # initialization and question collection
    ensure_data_directory("data")
    
    final_difficulty = difficulty_map[difficulty]

    new_quiz_data = {
        "title": title.strip(),
        "difficulty": final_difficulty,
        "questions": []
        }
    
    # question adding
    quiz_complete = add_questions(new_quiz_data)

    clear_screen()
    print_header()

    quiz_title = new_quiz_data.get("title")
    num_questions = len(new_quiz_data["questions"])
    
    # review (summary) and confirm
    print(color_yellow("\n--- QUIZ SUMMARY ---"))
    print(f"Title: {quiz_title}")
    print(f"Total Questions: {color_green(num_questions)}")
    print(color_yellow(f"----------------------\n"))

    while True:
        confirmation = input("Do you want to save this quiz? (y/n): ").strip().lower()

        if confirmation == "y":
            print(color_green("\nConfirmation accepted. Proceeding with saving..."))
            break
        elif confirmation == "n":
            print(color_red("\nSaving got cancelled by the user. Coming back to the main menu."))
            return None
        else:
            print(color_red(f"[ERROR] Invalid input. Insert 'y' or 'n'."))


    saved_path = save_quiz_to_file(new_quiz_data)

    return new_quiz_data

def add_questions(quiz_data):
    """
    this function lets the user add one or more questions to the quiz dictionary

    the function keeps running in a loop. it asks the user if they want to add a new question (y) or
    stop adding questions (n). if the user chooses 'n', it checks if at least one question has been added

    args:
    quiz_data (dict):   the quiz dictionary that is being created
                        it has a key called "questions" (which is an empty or partly filled list)
    
    returns:
    none: the function changes the 'quiz_data' dictionary directly
    
    """
    while True:
        # adding question management
        while True:
            print(color_blue("\n-") + color_blue("-") *34)
            print(color_green(f"Do you want to add Questions to your Quiz?"))
            print(color_blue("-" * 35))

            selection = input("Insert your answer (y/n): ").strip().lower()

            if selection == "n":
                # if no questions to be added, quit cycle
                break
            if selection == "y":
                print("\nOkay, let's proceed with adding a question...")
                # questions details collection function call
                collect_question_details(quiz_data)
            else:
                message = "Invalid input"
                error = color_red("[ERROR]")
                print(f"{error} {message}")
                continue

        # final check: if there is at least one question
        if len(quiz_data["questions"]) == 0:
            print(f"\nYou must insert at least one Question.")
            # if there are no questions, ask to add one
            continue
        else:
            # if there's at least one question, leave the cycle
            break

def collect_question_details(quiz_data):

    """
    the function interactively collects all the needed information for one single question
    (text, category, options, correct answers, points, limits) and adds it to the quiz

    the question ID is given automatically based on how many questions are already in the quiz

    args:
        quiz_data:  the quiz dictionary being created. this dictionary is changed by adding the new question
                    to the option list
    
    returns:
        None:       the function changes the 'quiz_data' dictionary directly
    """
    # text fields collection
    new_id = len(quiz_data["questions"])

    question = get_validated_text(prompt="Insert the Question: ", error_msg="Question cannot be empty.")

    category = get_validated_text(prompt="Insert the Category name: ", error_msg="Category cannot be empty.")

    # option collection
    option_list = collect_options_with_limit()

    # correct option collection
    correctOption = collect_and_validate_index(option_number = len(option_list))

    explanation = get_validated_text("Insert the Answer Explanation: ")

    points = collect_and_validate_int("Points to be assigned (e.g. 10): ", allow_zero = False)

    penalty = collect_and_validate_int("Penalty in case of Error (e.g. 2): ", allow_zero = False)
            
    time_limit = collect_and_validate_int("Time limit in seconds (e.g. 30): ", allow_zero = False)

    new_question = {
        "id": new_id,
        "question": question,
        "category": category,
        "options": option_list,
        "correctOption": correctOption,
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

def collect_and_validate_int(prompt, allow_zero):
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