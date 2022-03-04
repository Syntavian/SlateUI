# https://realpython.com/primer-on-python-decorators/
import functools
import inspect
import re
from typing import Iterable, Any

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

def redact_spacing(text: str) -> str:
    return re.sub(r"\s+", ' ', text)

def colour(_text: str, _colour: str = COLOURS["GREEN"], _reset: bool = True) -> str:
    return f"{_colour}{_text}{COLOURS['WHITE'] * _reset}"

def indent(_levels: int, _colour_offset: int = 0) -> str:
    return colour(f"{'|   ' * _levels}", COLOUR_MAP[(_levels + _colour_offset) % 3 + 3])

def redact_overflow(_text: str, _max_length: int = 100) -> str:
    if len(_text) > _max_length:
        return f"{_text[:98]}..."
    else:
        return _text

def repeat(_text: str, _times: int, _separator: str = '\n', _end: str = '') -> str:
    return f"{_text}{_separator}" * (_times - 1) + f"{_text}" + _end

def repeat_function(_function, _times: int, _args: Iterable[Iterable] = []) -> list:
    return [_function(*(_args[i])) for i in range(_times)]

def repeat_string_function(_function, _times: int, _args: Iterable[Iterable] = [], _separator: str = '\n', _end: str = '') -> str:
    return _separator.join(repeat_function(_function, _times, _args)) + _end

def format_value(_value: Any):
    return redact_overflow(redact_spacing(str(_value)))

def debug(_func):
    """Print the function signature and return value"""
    @functools.wraps(_func)
    def wrapper_debug(*args, **kwargs):
        global level
        arg_spec = inspect.getfullargspec(_func)
        args_repr = [f"{indent(level + 1)}{arg_spec[0][index]}={format_value(argument)}" for index, argument in enumerate(args)]                   
        kwargs_repr = [f"{indent(level + 1)}{key}={format_value(argument)}" for key, argument in kwargs.items()]  
        signature = ",\n".join(args_repr + kwargs_repr)           
        print(f"{repeat_string_function(indent, 2, [[level], (level, 1)])}{colour('> ', COLOURS['GREEN'])}{_func.__name__} called" + f" with:\n{signature}" * (not not signature))
        level += 1
        value = _func(*args, **kwargs)
        level -= 1
        print(f"{repeat_string_function(indent, 2, [[level + 1], (level, 1)])}{colour('< ', COLOURS['RED'])}{_func.__name__} returned {format_value(value)}")
        return value
    return wrapper_debug
