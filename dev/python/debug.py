# https://realpython.com/primer-on-python-decorators/
import functools
import inspect
import time
import re
from python.utils.string_utils import *
from python.utils.console_utils import *

WRITE_LOG_FILE = True

def write_debug_log(_text: str) -> None:
    print(_text)
    if WRITE_LOG_FILE:
        with open('debug.py.log', 'a') as log:
            for line in _text.split('\n'):
                log.write(re.sub(r".\[1;3.;40m", "", line + '\n'))

def debug(_func):
    """Print the function signature and return value"""
    @functools.wraps(_func)
    def wrapper_debug(*args, **kwargs):
        global level
        arg_spec = inspect.getfullargspec(_func)
        args_repr = [f"{indent(level + 1)}{arg_spec[0][index]} = {colour(format_value(argument), COLOURS['CYAN'])}" for index, argument in enumerate(args)]
        kwargs_repr = [f"{indent(level + 1)}{key} = {colour(format_value(argument), COLOURS['CYAN'])}" for key, argument in kwargs.items()]  
        signature = ",\n".join(args_repr + kwargs_repr)
        output = f"{repeat_string_function(indent, 2, [[level], (level, 1)])}{colour('>', COLOURS['GREEN'])} {colour(f'{_func.__name__}', COLOURS['CYAN'])} called" + f" with:\n{signature}" * (not not signature)
        write_debug_log(output)
        level += 1
        start_time = time.perf_counter()
        value = _func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        level -= 1
        output = f"{repeat_string_function(indent, 2, [[level + 1], (level, 1)])}{colour('<', COLOURS['RED'])} {colour(f'{_func.__name__}', COLOURS['CYAN'])} returned {colour(format_value(value), COLOURS['CYAN'])} in {colour(f'{run_time:.4f}', COLOURS['GREEN' if run_time < 0.1 else 'RED'])} secs"
        write_debug_log(output)
        return value
    return wrapper_debug
