import json
from pathlib import Path
from src.ui_terminal import print_top_10
from src.colors import color_cyan, color_green, color_red

def _get_storage_path():
    """
    this function figures out the full, exact path for the leaderboard save file ('leaderboard.json')

    the path is calculated starting from the main project folder (two levels up from this current file, assuming a normal project structure)

    returns:
        path: a path object that points to the file 'data/leaderboard.json'
    """
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    storage_file = project_root / "data" / "leaderboard.json"

    return storage_file

def load_leaderboard():
    """
    this function loads the leaderboard data from the specified JSON file

    it checks if the file exists and handles problems like bad JSON formatting or other input/output errors

    returns:
        list: a list of score records (it expects a list of dictionaries). it returns an empty list if the file is missing or broken
    """
    leaderboard_file = _get_storage_path()
    if not leaderboard_file.exists():
        message = "The file containing the Leaderboard data does not exist."
        info = color_cyan("[INFO]")
        print(f"{info} {message}")
        return []
    
    try:
        with leaderboard_file.open("r") as f:
            data = json.load(f)

            # checks if the loaded datas are in a list
            if isinstance(data, list):
                return data
            
    except json.JSONDecodeError:
        error = "[ERROR]"
        message = "The file containing the Leaderboard appears to be corrupted."
        print("{error} {message}")

        return []
    
    except Exception:
        # captures other kind of errors
        return []
    
def save_leaderboard(data_list):
    """
    this function saves the list of scores you give it into the leaderboard file.

    it makes sure the 'data' folder exists before trying to save the file

    args:
        data_list (list): the list of dictionaries that contains the leaderboard records to save

    returns:
        none: it prints a success message or an error message to the console 
    """
    leaderboard_file = _get_storage_path()
    leaderboard_directory = leaderboard_file
    leaderboard_directory.mkdir(parents=True, exist_ok=True)
    try:
        with leaderboard_file.open("w") as f:
            json.dump(data_list, f, indent=4)

        message = "Leaderboard data saved successfully."
        success = color_green("[SUCCESS]")
        print("{success} {message}")
    except Exception as e:
        error = color_red("[ERROR]")
        message = f"Could not save Leaderboard data: {e}"
        print(f"{error} {message}")

def display_top_10(quiz_name_filter):
    """
    
    this function loads all the scores, selects only the scores matching the specific quiz name, sorts the result,
    and then shows the top 10 scores using the special UI function

    args:
        quiz_name_filter (str): the name of the quiz to filter scores by
    """
    all_scores = load_leaderboard()

    filtered_scores = []

    for record in all_scores:
        # assuming that every record contains the keyword "quiz_name"
        if record["quiz_name"] == quiz_name_filter:
            filtered_scores.append(record)

    # order points by decrescent ordination 
    sorted_scores = sorted(filtered_scores, key = lambda item: item["score"], reverse = True)

    # takes only the first 10 results
    top_10 = sorted_scores[:10]

    # prints using the UI function
    print_top_10(top_10)