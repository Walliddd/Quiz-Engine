import sys 
from src.creator import run_quiz_creator
from src.engine import run_quiz
from src.data_manager import load_quiz_file, ensure_data_directory, load_quiz_data
from src.storage import load_leaderboard, save_leaderboard, display_top_10
from src.ui_terminal import clear_screen, print_header, get_username
from src.colors import color_blue, color_red, color_yellow, color_green, color_cyan


def display_main_menu():
    clear_screen()
    print_header()
    print(color_blue("\n" + "=" * 35))
    print(color_yellow("      MAIN MENU"))
    print(color_blue("=" * 35))
    print("1. Create a New Quiz")
    print("2. Play a Quiz")
    print("3. Exit application")
    print(color_blue("-" * 35))

def select_quiz_to_play(available_quizzes):
    """
    this funnction allows the user to select one quiz from the available list to play
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
    """

    while True:
        print(f"\n--- POST QUIZ ACTIONS ---")
        action = input(f"Do you want to view the Leaderboard for this quiz? (y/n): ").strip().lower()

        if action == "y":
            print(color_cyan(f"\nLoading Leaderboard for {quiz_title}..."))
            display_top_10(quiz_title)
            input(f"\nPress Enter to return to the Main Menu...")
            break
        if action == "n":
            break
        else:
            print(color_red(f"\n[ERROR] Invalid input. Enter 'y' or 'n'."))

def main_application_loop():
    """
    this function is the main loop to run the quiz application engine
    """

files = load_quiz_file()

print(f"Quiz found: {files}")

dati = load_quiz_data(files[0])

print(dati["title"])