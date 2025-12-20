from src.ui_terminal import display_question, get_answer

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

        user_answer = get_answer()
        correct_answer = question["correctOption"]

        

