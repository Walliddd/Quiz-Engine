from src.data_manager import load_quiz_file, load_quiz_data
from src.creator import save_new_quiz

save_new_quiz()

files = load_quiz_file()

print(f"Quiz found: {files}")

dati = load_quiz_data(files[0])

print(dati["title"])