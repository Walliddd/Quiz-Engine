import json
from pathlib import Path

def _get_storage_path():
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    storage_file = project_root / "data" / "leaderboard.json"

    return storage_file

def load_leaderboard():
    leaderboard_file = _get_storage_path()

    if not leaderboard_file.exists():
        print(f"[INFO] The file containing the Leaderboard data does not exist.")
        return []
    
    try:
        with leaderboard_file.open("r") as f:
            data = json.load(f)

            if isinstance(data, list):
                return data
            
    except json.JSONDecodeError:
        print("The file containing the Leaderboard appears to be corrupted.")

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

        print("[SUCCESS] Leaderboard data saved successfully.")
    except Exception as e:
        print(f"[ERROR] Could not save Leaderboard data: {e}")