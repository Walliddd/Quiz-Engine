# ANSI control constants
ESC = "\033" # escape character
RESET = f"{ESC}[0m" # sequence to reset formatting the terminal

# standard ANSI color codes
RED_CODE = 31
GREEN_CODE = 32
YELLOW_CODE = 33
BLUE_CODE = 34
MAGENTA_CODE = 35
CYAN_CODE = 36

def _apply_color(code, text):
    """
    this function adds a specific ANSI escape code before and after the text you give it

    args:
        code(int): the number code for the ANSI color you want to use (e.g., 31 for red)
        text (str): the text that need to be colored

    returns:
        str: the text wrapped with the start color code and the code to reset the color
    """
    return f"{ESC}[{code}m{text}{RESET}"

def color_red(text):
    """
    this function makes the text you give it turn red
    
    args:
        text(str): the text that need to be colored

    returns:
        str: the text colored red
    """
    return _apply_color(RED_CODE, text)

def color_green(text):
    """
    this function makes the text you give it turn green
    
    args:
        text(str): the text that need to be colored

    returns:
        str: the text colored green
    """
    return _apply_color(GREEN_CODE, text)

def color_yellow(text):
    """
    this function makes the text you give it turn yellow
    
    args:
        text(str): the text that need to be colored

    returns:
        str: the text colored yellow
    """
    return _apply_color(YELLOW_CODE, text)

def color_blue(text):
    """
    this function makes the text you give it turn blue
    
    args:
        text(str): the text that need to be colored

    returns:
        str: the text colored blue
    """
    return _apply_color(BLUE_CODE, text)

def color_magenta(text):
    """
    this function makes the text you give it turn magenta
    
    args:
        text(str): the text that need to be colored

    returns:
        str: the text colored magenta
    """
    return _apply_color(MAGENTA_CODE, text)

def color_cyan(text):
    """
    this function makes the text you give it turn cyan
    
    args:
        text(str): the text that need to be colored

    returns:
        str: the text colored cyan
    """
    return _apply_color(CYAN_CODE, text)