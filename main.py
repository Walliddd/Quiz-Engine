import sys 
from src.creator import run_quiz_creator
from src.engine import run_quiz
from src.data_manager import load_quiz_file, ensure_data_directory, load_quiz_data
from src.storage import load_leaderboard, save_leaderboard, display_top_10
from src.ui_terminal import clear_screen, print_header, get_username
from src.colors import color_blue, color_red, color_yellow


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

files = load_quiz_file()

print(f"Quiz found: {files}")

dati = load_quiz_data(files[0])

print(dati["title"])