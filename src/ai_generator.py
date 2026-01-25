import os
import json
import time
import getpass
from colors import color_red
import requests

def run_ai_quiz_generation(api_key, topic):
    """
    This function generates a quiz using AI and returns the quiz data

    Args:
        api_key: The API key for the AI service
        topic: The topic for the quiz to be generated

    Returns:
        The validated quiz data as a dictionary, or None if an error occurs.

    Raises:
        ValueError: if JSON parsing fails or the structure is invalid
        ConnectionError: if a network related error occurs during the request
    """
    API_ENDPOINT = "https://ai.hackclub.com/proxy/v1/chat/completions"
    HEADERS = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"Generate a quiz on the topic: {topic} with 12 multiple-choice questions. It must be as the structure: {{\"title\": str, \"difficulty\": str, \"questions\": [{{\"question\": str, \"options\": list, \"id\": int, \"correctOption\": int, \"explanation\": str, \"points\": int, \"penalty\": int, \"time_limit\": int, \"category\": str}}]}}"
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
    
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(color_red(f"[ERROR] Network/connection error: {str(e)}")) from e
    except requests.exceptions.Timeout as e:
        raise ConnectionError(color_red("[ERROR] The request to the AI service timed out.")) from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError(color_red(f"[ERROR] An error occurred while connecting to the AI service: {str(e)}")) from e
    
    return None


def ai_generator():
    """
    This function is the main entry point for the AI quiz generation module

    Returns: 
        The generated quiz data as a dictionary, or None if generation fails.
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
        return None
    except ConnectionError as ce:
        print(color_red(f"[ERROR] Connection error: {str(ce)}"))
        return None
    except Exception as e:
        print(color_red(f"[ERROR] Unknown error: {str(e)}"))
        return None



def _get_api_key_from_user():
    """
    This function takes user input to get the API key for AI services

    Returns:
        A tuple containing the API key and quiz topic

    Raises:
        ValueError: if the API key or topic is empty
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

    Args:
        quiz_data: the data returned by the AI service

    Returns:
        True if the structure is valid, False otherwise
    """
    
    if type(quiz_data) is not dict:
        return False
    
    if "title" not in quiz_data or not isinstance(quiz_data["title"], str):
        return False
    
    if "difficulty" not in quiz_data or not isinstance(quiz_data["difficulty"], str):
        return False
    
    if "questions" not in quiz_data or not isinstance(quiz_data["questions"], list) or not quiz_data["questions"]:
        return False
    
    for question in quiz_data["questions"]:
        if not isinstance(question, dict):
            return False
        
        required_keys = ["question", "options", "id", "correctOption", "explanation", "points", "penalty", "time_limit", "category"]

        if not all(key in question for key in required_keys):
            return False
        
        if not isinstance(question["question"], str):
            return False
        
        if not isinstance(question["question"], str):
            return False
        
        if not isinstance(question["options"], list) or not (len(question["options"]) >= 2):
            return False
        
        if not isinstance(question["correctOption"], int) or not (0<= question["correctOption"] < len(question["options"])):
            return False
        
        if not isinstance(question["explanation"], str):
            return False
        
        if not isinstance(question["points"], int) or question["points"] < 0:
            return False
        
        if not isinstance(question["penalty"], int):
            return False
        
        if not isinstance(question["time_limit"], int) or question["time_limit"] <= 0:
            return False
        
        if not isinstance(question["category"], str):
            return False
        
        if not isinstance(question["id"], int):
            return False
        
    return True