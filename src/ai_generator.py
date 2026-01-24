import os
import json
import time
from colors import color_red

def run_ai_quiz_generation():
    """
    This function generates a quiz using AI and returns the quiz data
    """
    pass

def ai_generator():
    """
    This function is the main entry point for the AI quiz generation module
    """
    pass

def _get_api_key_from_user():
    """
    This function takes user input to get the API key for AI services
    """
    key = input("Please enter your AI service API key (it won't be stored): ").strip()
    if not key:
        raise ValueError(f"{color_red("[ERROR] API key cannot be empty.")}")
    
    topic = input("Please, enter the quiz topic you want to generate:").strip()
    if not topic:
        raise ValueError(f"{color_red("[ERROR] Quiz topic cannot be empty.")}")
    
    return key, topic