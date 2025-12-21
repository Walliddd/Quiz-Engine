from src.ui_terminal import display_question, get_answer, clear_screen, print_header
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

        try:
            user_index = string.ascii_uppercase().index(user_answer)
        except ValueError:
            user_index = -1

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

    return match_status

def show_results(match_status):
    clear_screen()
    print_header()
    print("\n-","-" *34)
    print("Quiz Completed!")
    print("-" * 35)

    print(f"\n- Total Score: {match_status["score"]}")
    print(f"- Correct Answers: {match_status["correct_answers"]}/{match_status["total_questions"]}")
    print(f"- Incorrect Answers: {match_status["incorrect_answers"]}/{match_status["total_questions"]}")

    if match_status["correct_answers"] > match_status["incorrect_answers"]:
        print(f"\nGood job!")
    else:
        print(f"\nToo bad, try again!")