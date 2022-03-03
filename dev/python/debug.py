# https://realpython.com/primer-on-python-decorators/
import functools
import inspect
import re

level = 0

def redact_spacing(text: str) -> str:
    return re.sub(r"\s+", ' ', text)

def debug(_func):
    """Print the function signature and return value"""
    @functools.wraps(_func)
    def wrapper_debug(*args, **kwargs):
        global level
        arg_spec = inspect.getfullargspec(_func)
        args_repr = [f"\033[1;3{level % 3 + 3};40m{'|   ' * (level + 1)}\033[1;37;40m{arg_spec[0][i]}={redact_spacing(str(a))}" if len(redact_spacing(str(a))) < 100 else f"\033[1;3{level % 3 + 3};40m{'|   ' * (level + 1)}\033[1;37;40m{arg_spec[0][i]}={redact_spacing(str(a))[:98]}..." for i, a in enumerate(args)]                   
        kwargs_repr = [f"\033[1;3{level % 3 + 3};40m{'|   ' * (level + 1)}\033[1;37;40m{k}={redact_spacing(str(v))}" if len(redact_spacing(str(v))) < 100 else f"\033[1;3{level % 3 + 3};40m{'|   ' * (level + 1)}\033[1;37;40m{k}={redact_spacing(str(v))[:98]}..." for k, v in kwargs.items()]  
        signature = ",\n".join(args_repr + kwargs_repr)           
        if signature: print(f"\033[1;3{(level - 1) % 3 + 3};40m{'|   ' * (level)}\n\033[1;3{level % 3 + 3};40m{'|   ' * (level)}\033[1;32;40m>\033[1;37;40m {_func.__name__} called with:\n{signature}")
        else: print(f"\033[1;3{(level - 1) % 3 + 3};40m{'|   ' * (level)}\n\033[1;3{level % 3 + 3};40m{'|   ' * (level)}\033[1;32;40m>\033[1;37;40m {_func.__name__} called")
        level += 1
        value = _func(*args, **kwargs)
        level -= 1
        if len(redact_spacing(str(value))) < 100: print(f"\033[1;3{level % 3 + 3};40m{'|   ' * (level + 1)}\n\033[1;3{level % 3 + 3};40m{'|   ' * (level)}\033[1;31;40m<\033[1;37;40m {_func.__name__!s} returned {redact_spacing(str(value))}")
        else: print(f"\033[1;3{level % 3 + 3};40m{'|   ' * (level + 1)}\n\033[1;3{level % 3 + 3};40m{'|   ' * (level)}\033[1;31;40m<\033[1;37;40m {_func.__name__!s} returned {redact_spacing(str(value))[:98]}...")
        return value
    return wrapper_debug