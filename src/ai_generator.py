import os
import json
import time
import getpass
from src.colors import color_red, color_green, color_blue, color_yellow, color_magenta
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
    json_structure_example = json.dumps({
        "title": "Topic Title",
        "difficulty": "Medium",
        "questions": [
            {
                "question": "Example question?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "id": 0,
                "correctOption": 1, 
                "explanation": "Explanation here",
                "points": 10,
                "penalty": 5,
                "time_limit": 20,
                "category": "Topic Name"
            }
        ]
    })

    system_instruction = (
        "You are a strict JSON generator for a quiz engine. "
        "Output ONLY raw JSON data. Do not use Markdown formatting (no ```json). "
        "Do not include any introductory text. "
        f"Follow this exact JSON structure: {json_structure_example}"
    )

    API_ENDPOINT = "https://ai.hackclub.com/proxy/v1/chat/completions"
    HEADERS = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Generate a quiz on the topic: '{topic}' with 12 multiple-choice questions. "
        "Ensure 'correctOption' is the 0-based index of the correct answer in the 'options' list. "
        "Ensure 'id' is a sequential integer starting from 0. "
        "Vary the difficulty, points, and time_limit appropriately."
    )

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
                {"role": "system", "content": system_instruction},
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
            api_response = response.json()
            try:
                content_string = api_response["choices"][0]["message"]["content"]
            except (KeyError, IndexError) as e:
                raise ValueError("Unexpected API response format (missing choices/message)")
            
            if content_string.startswith("```json"):
                content_string = content_string.replace("```json", "").replace("```", "")
            elif content_string.startswith("```"):
                content_string = content_string.replace("```", "")

            content_string = content_string.strip()

            try:
                quiz_data = json.loads(content_string)
            except json.JSONDecodeError as e:
                print(color_yellow(f"[DEBUG] Raw AI Output that failed parsing:\n{content_string}"))
                raise ValueError(color_red(f"[ERROR] Failed to parse AI response as JSON: {str(e)}"))
            
            if validate_ai_quiz_structure(quiz_data):
                return quiz_data
            else:
                print(color_yellow(f"[DEBUG] Invalid JSON structure received:\n{json.dumps(quiz_data, indent=2)}"))
                raise ValueError(color_red("[ERROR] AI-generated quiz data has an invalid structure."))
            
        elif response.status_code in [401, 403]:
            raise ValueError(color_red("[ERROR] Authentication failed. Please check your API key."))
        else:
            raise ValueError(color_red(f"[ERROR] Error in AI service server. Status code: {response.status_code}. Message: {response.text}"))
    
    except requests.exceptions.RequestException as e:
        raise ConnectionError(color_red(f"[ERROR] Network/connection error: {str(e)}")) from e
    
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