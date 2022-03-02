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
        args_repr = [f"{'|   ' * (level + 1)}{arg_spec[0][i]}={redact_spacing(str(a))}" if len(redact_spacing(str(a))) < 100 else f"{'|   ' * (level + 1)}{arg_spec[0][i]}={redact_spacing(str(a))[:98]}..." for i, a in enumerate(args)]                   
        kwargs_repr = [f"{'|   ' * (level + 1)}{k}={redact_spacing(str(v))}" if len(redact_spacing(str(v))) < 100 else f"{'|   ' * (level + 1)}{k}={redact_spacing(str(v))[:98]}..." for k, v in kwargs.items()]  
        signature = ",\n".join(args_repr + kwargs_repr)           
        if signature: print(f"{'|   ' * (level)}\n{'|   ' * (level)}> {_func.__name__} called with:\n{signature}")
        else: print(f"{'|   ' * (level)}\n{'|   ' * (level)}> {_func.__name__} called")
        level += 1
        value = _func(*args, **kwargs)
        level -= 1
        if len(redact_spacing(str(value))) < 100: print(f"{'|   ' * (level + 1)}\n{'|   ' * (level)}< {_func.__name__!s} returned {redact_spacing(str(value))}")
        else: print(f"{'|   ' * (level + 1)}\n{'|   ' * (level)}< {_func.__name__!s} returned {redact_spacing(str(value))[:98]}...")
        return value
    return wrapper_debug