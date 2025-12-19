import os
import platform
from typing import List, Dict

def print_welcome():
    pass

def show_menu(quiz_list):
    for quiz in quiz_list:
        print(f"[{quiz["id"]}] {quiz["title"]}")

def get_user_choice(max_option):
    while True:
        clear_screen()
        print_header()
        print(f"Scegli un'opzione tra ")

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")

    else:
        os.system("clear")

def print_header():
    header = """ # ascii art font name 'Classy'
                                                                  
   ▄▄▄▄                         ▄▄▄▄▄▄▄                           
 ▄█▀▀███▄▄                     █▀██▀▀▀                            
 ██    ██       ▀▀               ██     ▄        ▄▄ ▀▀ ▄          
 ██    ██ ██ ██ ██ ▀▀▀██         ████   ████▄ ▄████ ██ ████▄ ▄█▀█▄
 ██  ▄ ██ ██ ██ ██   ▄█▀ ▀▀▀▀    ██     ██ ██ ██ ██ ██ ██ ██ ██▄█▀
  ▀█████▄▄▀██▀█▄██▄▄██▄▄         ▀█████▄██ ▀█▄▀████▄██▄██ ▀█▄▀█▄▄▄
       ▀█                                        ██               
                                               ▀▀▀                """

def display_question():
    pass 