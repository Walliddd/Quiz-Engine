from src.ui_terminal import display_question, get_answer, clear_screen, print_header, get_username
import string
from datetime import datetime
from src.storage import save_leaderboard, load_leaderboard
from src.colors import color_blue, color_cyan, color_green, color_magenta, color_red, color_yellow
import time

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

        base_points = question["points"]
        time_limit = question.get("time_limit", 0)
        

        option_list = question["options"]

        start_time = time.perf_counter()
        user_answer = get_answer()
        end_time = time.perf_counter()

        time_taken_raw = end_time - start_time
        time_taken_rounded = round(time_taken_raw, 1)

        try:
            user_index = string.ascii_uppercase.index(user_answer)
        except ValueError:
            user_index = -1

        correct_answer = question["correctOption"]

        if user_index == correct_answer:
            points_gained, feedback_message = calculate_score(base_points, time_taken_rounded, time_limit)
            match_status["score"] += points_gained

            match_status["correct_answers"] += 1

            if points_gained > base_points:
                print(color_green(f"CORRECT! {feedback_message}"))
            elif points_gained == base_points:
                print(color_green(f"Correct! Time taken: {time_taken_rounded}s."))
            elif points_gained == 0 and time_limit > 0:
                print(color_red(f"Attention! {feedback_message} (Points: 0)"))

            print(color_green(f"\nExplanation: {question["explanation"]}"))
        else:
            match_status["incorrect_answers"] += 1
            penalty = question.get("penalty", 0)
            match_status["score"] -= penalty

            print(color_magenta(f"Too bad! Your answer wasn't correct! It was the option '{option_list[correct_answer]}'"))

    input("\nPress Enter to proceed...")
    show_results(match_status)

    input("\nPress Enter to proceed...")
    username = get_username()
    current_date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    score_record = {
        "username": username,
        "score": match_status["score"],
        "quiz_name": quiz_data["title"],
        "date": current_date_str
    }

    all_leaderboard_data = load_leaderboard()

    all_leaderboard_data.append(score_record)
    save_leaderboard(all_leaderboard_data)

    return match_status

def show_results(match_status):
    clear_screen()
    print_header()
    print(color_blue("\n-") + color_blue("-") *34)
    print("Quiz Completed!")
    print(color_blue("-") * 35)

    print(f"\n- Total Score: {match_status["score"]}")
    print(f"- Correct Answers: {match_status["correct_answers"]}/{match_status["total_questions"]}")
    print(f"- Incorrect Answers: {match_status["incorrect_answers"]}/{match_status["total_questions"]}")

    if match_status["total_questions"] > 0:
        percentual = (match_status["correct_answers"] / match_status["total_questions"]) * 100
    else:
        percentual = 0.0

    if percentual >= 90:
        print(f"\nExcellent! Amazing performance! You're an expert")
    elif percentual >= 70:
        print(f"\nGood job! You have a solid understanding of the topic.")
    elif percentual >= 50:
        print(f"\nDecent. There's room for improvement, but you're over the halfway mark")
    elif percentual >= 30:
        print(f"You need to see some key concepts.")
    else:
        print(f"\nToo bad, try again!")

def calculate_score(base_points, time_taken, time_limit):
    if time_limit == 0 or time_limit is None:
        return (base_points, "Correct Answer, no time limit applied.")
    
    if time_taken > time_limit:
        final_points = 0
        message = f"Too slow! You took {time_taken:.1f}s, the limit was {time_limit}s."
        return (final_points, message)
    
    bonus_time_threshold = time_limit / 2

    if time_taken <= bonus_time_threshold:
        bonus_points = 10
        final_points = base_points + bonus_points
        message = f"Rapid response! You got a bonus of {bonus_points} points."
        return (final_points, message)
    else:
        final_points = base_points
        message = f"Answer correct standard."
        return (final_points, message)