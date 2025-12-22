import json
from pathlib import Path
from src.ui_terminal import print_top_10
from src.colors import color_yellow, color_blue, color_cyan, color_green, color_magenta, color_red

def _get_storage_path():
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    storage_file = project_root / "data" / "leaderboard.json"

    return storage_file

def load_leaderboard():
    leaderboard_file = _get_storage_path()

    if not leaderboard_file.exists():
        message = "The file containing the Leaderboard data does not exist."
        info = color_cyan("[INFO]")
        print(f"{info} {message}")
        return []
    
    try:
        with leaderboard_file.open("r") as f:
            data = json.load(f)

            if isinstance(data, list):
                return data
            
    except json.JSONDecodeError:
        error = "[ERROR]"
        message = "The file containing the Leaderboard appears to be corrupted."
        print("{error} {message}")

        return []
    
    except Exception:
        return []
    
def save_leaderboard(data_list):
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
    all_scores = load_leaderboard()

    filtered_scores = []

    for record in all_scores:
        if record["quiz_name"] == quiz_name_filter:
            filtered_scores.append(record)

    sorted_scores = sorted(filtered_scores, key = lambda item: item["score"], reverse = True)

    top_10 = sorted_scores[:10]

    print_top_10(top_10)