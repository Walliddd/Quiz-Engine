from src.ui_terminal import display_question, get_answer, clear_screen
import string

def run_quiz(quiz_data):
    match_status = {

        "score": 0,
        "correct_answers": 0,
        "incorrect_answers": 0,
        "total_questions": 0,
        "current_question_index": 0
    }

    total_questions = len(quiz_data["questions"])
    match_status["total_questions"] = total_questions

    for question in quiz_data["questions"]:
        display_question(question)

        option_list = question["options"]
        user_answer = get_answer()
        correct_answer = question["correctOption"]

        letter_to_index = {}

        for index in range(len(option_list)):
            if index < len(string.ascii_uppercase):
                letter = string.ascii_uppercase[index]
                letter_to_index[letter] = index
            else:
                break

        user_index = letter_to_index.get(user_answer, -1)

        if user_index == correct_answer:
            match_status["correct_answers"] += 1
            points = question["points"]
            match_status["score"] += points

            print(f"\nCongratulations! Your answer is correct! \nExplanation: {question["explanation"]}")
        else:
            match_status["incorrect_answers"] += 1
            penalty = question.get("penalty", 0)
            match_status["score"] -= penalty

            print(f"Too bad! Your answer wasn't correct! It was the option '{option_list[correct_answer]}'")

def show_results():
