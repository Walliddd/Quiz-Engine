from src.ui_terminal import display_question, get_answer, clear_screen, print_header, get_username
import string
from datetime import datetime
from src.storage import save_leaderboard, load_leaderboard
from src.colors import color_blue, color_cyan, color_green, color_magenta, color_red, color_yellow
import time
import random 

def run_quiz(quiz_data):
    """
    this function runs the main part of the quiz: it shows the questions in a mixed order, manages how long
    the user takes to answer, calculates the points, and records the final result

    args:
        quiz_data (dict):   a dictionary containing the quiz structure, including the title and the list
                            of questions
            
    returns:
        dict or None:       the final match status (score, correct/incorrect answers)
                            it returns none if the process stops early (even though the current plan doesn't seem to allow for an easy stop)
    """
    match_status = {

        "score": 0,
        "correct_answers": 0,
        "incorrect_answers": 0,
        "total_questions": 0,
        "current_question_index": 0
    }

    total_questions = len(quiz_data["questions"])
    match_status["total_questions"] = total_questions

    question_list_original = quiz_data["questions"]

    question_to_shuffle = question_list_original.copy()

    random.shuffle(question_to_shuffle)

    for i, question in enumerate(question_to_shuffle):
        question_number = i + 1
        display_question(question, question_number, total_questions)

        base_points = question["points"]
        time_limit = question.get("time_limit", 0)
        

        option_list = question["options"]

        # time measurement
        start_time = time.perf_counter()
        user_answer = get_answer() # takes user input 
        end_time = time.perf_counter()

        time_taken_raw = end_time - start_time
        time_taken_rounded = round(time_taken_raw, 1)
        
        # conversion of the answer
        try:
            user_index = string.ascii_uppercase.index(user_answer)
        except ValueError:
            user_index = -1 # as invalid format

        correct_answer = question["correctOption"]

        if user_index == correct_answer:
            # correct answer
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
            # wrong answer
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
    """
    this function show a summary of the results on the screen when the quiz ends

    it calculates the total score, the number of correct/incorrect answers, and gives some text feedback based on how many answers were right

    args:
        match_status (dict): a dictionary containing score, correct_answers, incorrect_answers, and total_questions
    """
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
    """
    this function calculates the final points for a correct answer
    it also adds bonus points or considers penalties based on the time limit, if there is one

    args:
        base_points (int): the points given for the correct answer without time bonuses or penalties
        time_taken (float): the time user spent answering in seconds
        time_limit (int): the maximum time limit to get the bonus in seconds

    returns:
        tuple[int, str]: a pair containing (final_points, feedback_message)
    """
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