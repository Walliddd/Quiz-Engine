ESC = "\033"
RESET = f"{ESC}[0m"

RED_CODE = 31
GREEN_CODE = 32
YELLOW_CODE = 33
BLUE_CODE = 34
MAGENTA_CODE = 35
CYAN_CODE = 36

def _apply_color(code, text):
    return f"{ESC}[{code}m{text}{RESET}"

def color_red(text):
    return _apply_color(RED_CODE, text)

def color_green(text):
    return _apply_color(GREEN_CODE, text)

def color_yellow(text):
    return _apply_color(YELLOW_CODE, text)

def color_blue(text):
    return _apply_color(BLUE_CODE, text)

def color_magenta(text):
    return _apply_color(MAGENTA_CODE, text)

def color_cyan(text):
    return _apply_color(CYAN_CODE, text)