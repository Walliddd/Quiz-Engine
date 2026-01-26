import os
import json
import time
from src.colors import color_red, color_green, color_blue, color_yellow, color_magenta, color_cyan
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
    example_structure = json.dumps({
        "title": "Syntax and basic Python concepts.",
        "difficulty": "Easy",
        "questions": [
            {
                "question": "What keyword is used to define a function?",
                "options": ["func", "define", "def", "function"],
                "id": 0,
                "correctOption": 2,
                "explanation": "'def' is short for define",
                "points": 10,
                "penalty": 5,
                "time_limit": 20,
                "category": "Programming"
            }
        ]
    })

    system_instruction = (
        "You are a strict JSON generator for a quiz engine. "
        "Output ONLY raw JSON data. Do not use Markdown formatting (no ```json). "
        "Do not include any introductory text. "
        f"Follow this exact JSON structure: {example_structure}"
    )

    
    model_name = "gemini-2.5-flash-lite-preview-09-2025" 
    API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    HEADERS = {"Content-Type": "application/json"}


    prompt = (
        f"Generate a quiz on the topic: '{topic}' with 12 multiple-choice questions. "
        "Strictly output raw JSON matching this structure exactly. \n"
        f"Structure Example: {example_structure}\n\n"
        "Rules:\n"
        "1. 'correctOption' must be the index (0-3) of the correct answer.\n"
        "2. 'options' must be a list of 4 strings.\n"
        "3. 'id' must be sequential starting from 0.\n"
        "4. No Markdown, no code blocks, just JSON."
    )

    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.4,
            "response_mime_type": "application/json" 
        }
    }
    try:
        response = requests.post(API_ENDPOINT, headers=HEADERS, json=payload, timeout=30)

        if response.status_code == 200:
            api_response = response.json()
            try:
                content_string = api_response["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError) as e:
                print(color_yellow(f"[DEBUG] Full Response: {response}"))
                raise ValueError("Unexpected API response format (missing candidates/message)")

            content_string = content_string.strip()
            if content_string.startswith("```json"):
                content_string = content_string[7:]
            if content_string.startswith("```"):
                content_string = content_string[3:]
            if content_string.endswith("```"):
                content_string = content_string[:-3]
            
            content_string = content_string.strip()

            try:
                quiz_data = json.loads(content_string)
            except json.JSONDecodeError as e:
                print(color_yellow(f"[DEBUG] Raw AI Output that failed parsing:\n{content_string}"))
                raise ValueError(color_red(f"[ERROR] Failed to parse AI response as JSON: {str(e)}"))
            
            if validate_ai_quiz_structure(quiz_data):
                return quiz_data
            else:
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
        print(color_blue(f"Generating quiz on '{topic}'... This may take up to a minute."))

        quiz_data = run_ai_quiz_generation(key, topic)

        if quiz_data:
            print(color_green("[SUCCESS] Quiz generated successfully"))
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
    print(color_magenta("To generate a quiz using AI, an API key for the AI service is required.\n\n"))
    print(color_cyan("ENTER A VALID GEMINI API KEY TO PROCEED.\n"))
    key = input("Please enter your AI service API key (it won't be stored): ").strip()
    if not key:
        raise ValueError(f"{color_red("[ERROR] API key cannot be empty.")}")
    
    topic = input("Please, enter the quiz topic you want to generate: ").strip()
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
        print(color_yellow("[DEBUG Validation] Root is not a dictionary."))
        return False
    
    if "title" not in quiz_data or not isinstance(quiz_data["title"], str):
        print(color_yellow("[DEBUG Validation] Missing or invalid 'title'."))
        return False
    
    if "difficulty" not in quiz_data or not isinstance(quiz_data["difficulty"], str):
        print(color_yellow("[DEBUG Validation] Missing or invalid 'difficulty'."))
        return False
    
    if "questions" not in quiz_data or not isinstance(quiz_data["questions"], list) or not quiz_data["questions"]:
        print(color_yellow("[DEBUG Validation] 'questions' list is missing, empty, or not a list."))
        return False
    
    required_keys = ["question", "options", "id", "correctOption", "explanation", "points", "penalty", "time_limit", "category"]

    for i, question in enumerate(quiz_data["questions"]):
        if not isinstance(question, dict):
            print(color_yellow(f"[DEBUG Validation] Item at index {i} in questions is not a dict."))
            return False

        missing_keys = [key for key in required_keys if key not in question]
        if missing_keys:
            print(color_yellow(f"[DEBUG Validation] Question {i} missing keys: {missing_keys}"))
            return False
        
        if not isinstance(question["question"], str):
            print(color_yellow(f"[DEBUG] Question {i}: 'question' is not str"))
            return False
        
        if not isinstance(question["options"], list) or len(question["options"]) < 2:
            print(color_yellow(f"[DEBUG] Question {i}: 'options' invalid (must be list >= 2)"))
            return False
            
        if not isinstance(question["correctOption"], int):
            print(color_yellow(f"[DEBUG] Question {i}: 'correctOption' is not int"))
            return False

        if not (0 <= question["correctOption"] < len(question["options"])):
            print(color_yellow(f"[DEBUG] Question {i}: 'correctOption' index out of range"))
            return False

        if not isinstance(question["points"], int):
            print(color_yellow(f"[DEBUG] Question {i}: 'points' is not int"))
            return False

        if not isinstance(question["id"], int):
            print(color_yellow(f"[DEBUG] Question {i}: 'id' is not int"))
            return False

    return True