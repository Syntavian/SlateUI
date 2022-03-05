COLOURS = {
    "BLACK": "\033[1;30;40m",
    "RED": "\033[1;31;40m",
    "GREEN": "\033[1;32;40m",
    "YELLOW": "\033[1;33;40m",
    "BLUE": "\033[1;34;40m",
    "PURPLE": "\033[1;35;40m",
    "CYAN": "\033[1;36;40m",
    "WHITE": "\033[1;37;40m",
}

COLOUR_MAP = {
    0: COLOURS["BLACK"],
    1: COLOURS["RED"],
    2: COLOURS["GREEN"],
    3: COLOURS["YELLOW"],
    4: COLOURS["BLUE"],
    5: COLOURS["PURPLE"],
    6: COLOURS["CYAN"],
    7: COLOURS["WHITE"],
}

level = 0

def colour(_text: str, _colour: str = COLOURS["GREEN"], _reset: bool = True) -> str:
    return f"{_colour}{_text}{COLOURS['WHITE'] * _reset}"

def indent(_levels: int, _colour_offset: int = 0) -> str:
    return colour(f"{'|   ' * _levels}", COLOUR_MAP[(_levels + _colour_offset) % 3 + 3])
