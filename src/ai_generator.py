import os
import json
import time
import getpass
from colors import color_red
import requests

def run_ai_quiz_generation(api_key, topic):
    """
    This function generates a quiz using AI and returns the quiz data
    """
    API_ENDPOINT = "https://ai.hackclub.com/proxy/v1/chat/completions"
    HEADERS = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"Generate a quiz on the topic: {topic} with 12 multiple-choice questions. It must be as the structure: {\"title\": str, \"difficulty\": str, \"questions\": [{\"question\": str, \"options\": list, \"id\": int, \"correctOption\": int, \"explanation\": str, \"points\": int, \"penalty\": int, \"time_limit\": int, \"category\": str}]}"
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
                {"role": "system", "content": "You are a helpful assistant that generates quizzes."},
                {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
    }
    try:
        response = requests.post(
            url = API_ENDPOINT,
            headers = HEADERS,
            json = payload,
            timeout = 30
        )

        if response.status_code == 200:
            try:
                quiz_data = response.json()
            except json.JSONDecodeError:
                raise ValueError("Failed to parse AI response as JSON.")
            
            if validate_ai_quiz_structure(quiz_data):
                return quiz_data
            else:
                raise ValueError(color_red("[ERROR] AI-generated quiz data has an invalid structure."))
            
        elif response.status_code == 401 or response.status_code == 403:
            raise ValueError(color_red("[ERROR] Authentication failed. Please check your API key."))
        else:
            raise ValueError(color_red(f"[ERROR] Error in AI service server. Status code: {response.status_code}"))
        
        raise ConnectionError(color_red(f"[ERROR] Net connection Error."))
    
    except requests.exceptions.RequestException as e:
        raise ConnectionError(color_red(f"[ERROR] Connection error: {str(e)}"))
    
    return None


def ai_generator():
    """
    This function is the main entry point for the AI quiz generation module
    """
    try:
        key, topic = _get_api_key_from_user()
        quiz_data = run_ai_quiz_generation(key, topic)

        if quiz_data:
            print("Quiz generated successfully")
            return quiz_data
        else:
            return None
    except ValueError as ve:
        print(color_red(str(ve)))
    except requests.exceptions.RequestException as re:
        print(color_red(f"[ERROR] Connection error: {str(re)}"))
    except Exception as e:
        print(color_red(f"[ERROR] Unknown error: {str(e)}"))



def _get_api_key_from_user():
    """
    This function takes user input to get the API key for AI services
    """
    key = getpass.getpass("Please enter your AI service API key (it won't be stored): ").strip()
    if not key:
        raise ValueError(f"{color_red("[ERROR] API key cannot be empty.")}")
    
    topic = input("Please, enter the quiz topic you want to generate:").strip()
    if not topic:
        raise ValueError(f"{color_red("[ERROR] Quiz topic cannot be empty.")}")
    
    return key, topic

def validate_ai_quiz_structure(quiz_data):
    """
    This function validates the structure of the AI-generated quiz data.
    """
    