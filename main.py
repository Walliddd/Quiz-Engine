import sys 
from src.creator import run_quiz_creator, sanitize_title_for_filename, save_quiz_to_file
from src.engine import run_quiz
from src.data_manager import load_quiz_file, ensure_data_directory, load_quiz_data
from src.storage import load_leaderboard, save_leaderboard, display_top_10
from src.ui_terminal import clear_screen, print_header, get_username
from src.colors import color_blue, color_red, color_yellow, color_green, color_cyan
from src.ai_generator import ai_generator, validate_ai_quiz_structure


def display_main_menu():
    """
    this function shows the main menu to the user

    returns:
        None
    """
    clear_screen()
    print_header()
    print(color_blue("\n" + "=" * 35))
    print(color_yellow("      MAIN MENU"))
    print(color_blue("=" * 35))
    print("1. Create a New Quiz")
    print("2. Play a Quiz")
    print("3. Generate Quiz using AI")
    print("4. Exit application")
    print(color_blue("-" * 35))

def select_quiz_to_play(available_quizzes):
    """
    this funnction allows the user to select one quiz from the available list to play

    args:
        available_quizzes (list[str]): a list of strings with the names of the valid JSON quiz files
    
    returns:
        str or None: the filename of the selected quiz, or None if the user wants to go back to the main menu
    """

    if not available_quizzes:
        print(color_yellow(f"\n[INFO] No valid quizzes found to play."))
        print(f"\nPress Enter to return to the menu...")

        return None
    
    clear_screen()
    print_header()
    print(color_blue(f"\n--- SELECT QUIZ TO PLAY ---"))

    # displays available quizzes

    for i, filename in enumerate(available_quizzes):
        print(f"{i + 1}. {filename}")

    print(color_blue("-" * 35))

    while True:
        choice = input("\nEnter the number of the quiz you want to play (or 'b' to go back): ").strip().lower()

        if choice == "b":
            return None
        
        try:
            index = int(choice) - 1

            if 0 <= index < len(available_quizzes):
                selected_filename = available_quizzes[index]
                print(color_green(f"\nYou selected: {selected_filename}"))

                return selected_filename
            else:
                print(color_red(f"\n[ERROR] Invalid number. Please choose from the list."))
        except ValueError:
            print(color_red(f"\n[ERROR] Invalid input. Enter a number or 'b'."))

def load_selected_quiz(filename):
    """
    this function loads quiz data from the specified file using data_manager 

    args:
        filename (str): the name of the JSON file to load (it must be in 'data/')

    returns:
        dict or None: the content of the JSON file loaded as a python dictionary, or None if loading fails
    """
    try:
        quiz_data = load_quiz_data(filename)

        return quiz_data
    except Exception as e:
        print(color_red(f"\n[CRITICAL ERROR] Could not load quiz data for {filename}: {e}"))
        input(f"Press Enter to continue...")
        
        return None
    
def handle_post_quiz_actions(quiz_title):
    """
    this function handles viewing the leaderboard after a quiz section

    
    args:
        quiz_title (str): the title of the quiz just played

    returns:
        none

    """

    while True:
        print(f"\n--- POST QUIZ ACTIONS ---")
        action = input(f"Do you want to view the Leaderboard for this quiz? (y/n): ").strip().lower()

        if action == "y":
            print(color_cyan(f"\nLoading Leaderboard for {quiz_title}..."))
            display_top_10(quiz_title)
            break
        if action == "n":
            break
        else:
            print(color_red(f"\n[ERROR] Invalid input. Enter 'y' or 'n'."))

def main_application_loop():
    """
    this function is the main loop to run the quiz application engine

    args:
        none    
    
    returns:
        none
    """

    ensure_data_directory("data")

    available_quizzes = load_quiz_file()

    while True:
        display_main_menu()

        available_quizzes = load_quiz_file()

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            print(color_blue(f"\nStarting Quiz Creator..."))
            run_quiz_creator()

            available_quizzes = load_quiz_file()

        elif choice == "2":
            selected_file = select_quiz_to_play(available_quizzes)

            if selected_file:
                quiz_data = load_quiz_data(selected_file)

                if quiz_data:
                    quiz_title = quiz_data["title"]
                    print(color_blue(f"\nStarting Quiz: {quiz_title}"))

                    match_status = run_quiz(quiz_data)

                    if match_status:
                        handle_post_quiz_actions(quiz_title)

        elif choice == "3":
            print(color_blue(f"Starting AI Quiz Generation..."))

            quiz_data_ai = ai_generator()

            if quiz_data_ai is not None:
                ai_quiz_title = sanitize_title_for_filename(quiz_data_ai["title"])

                saved_path = save_quiz_to_file(quiz_data_ai)

                if saved_path is not None:
                    print(color_green(f"\nAI-generated quiz saved successfully as {saved_path}."))
                else:
                    print(color_red(f"\n[ERROR] Failed to save the AI-generated quiz."))


        
        elif choice == "4":
            print(color_green(f"\nThank you for using the Quiz App. Goodbye!"))
            sys.exit(0)

        else:
            print(color_red(f"[ERROR] Invalid choice. Please select 1, 2, 3, or 4."))

        input(f"\nPress Enter to return to the Main Menu")

try:
    ensure_data_directory("data")
    main_application_loop()
except KeyboardInterrupt:
    print(color_red(f"\n\nApplication interrupted by user (Ctrl+C). Exiting."))
    sys.exit(0)