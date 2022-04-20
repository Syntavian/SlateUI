from typing import Any
from python.utils.string_utils import format_value

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


def indent(_levels: int = 1) -> str:
    return f"{'|   ' * _levels}"


def coloured_indent(_levels: int = 1, _colour_offset: int = 0) -> str:
    return colour(indent(_levels), COLOUR_MAP[(_levels + _colour_offset) % 3 + 3])


def describe(_variable_name: str, _variable_value: Any):
    return f"{_variable_name}: {format_value(_variable_value)},"


def describe_class(_class_name: str, **_kwargs):
    args_representation = ""
    for key in _kwargs:
        if isinstance(_kwargs[key], list):
            args_representation += f"\n{indent()}{key}:"
            for value in _kwargs[key]:
                for line in f"{value}".split("\n"):
                    args_representation += f"\n{indent(2)}{line}"
        else:
            args_representation += f"\n{indent()}{describe(key, _kwargs[key])}"
    return f"{_class_name} <{args_representation}\n>"
