# https://realpython.com/primer-on-python-decorators/
import functools
import inspect

level = 0

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        global level
        arg_spec = inspect.getfullargspec(func)
        args_repr = [f"{'|   ' * (level + 1)}{arg_spec[0][i]}={a!r}" if len(repr(a)) < 100 else f"{'|   ' * (level + 1)}{arg_spec[0][i]}={repr(a)[:98]}..." for i, a in enumerate(args)]                   
        kwargs_repr = [f"{'|   ' * (level + 1)}{k}={v!r}" if len(repr(v)) < 100 else f"{'|   ' * (level + 1)}{k}={repr(v)[:98]}..." for k, v in kwargs.items()]  
        signature = ",\n".join(args_repr + kwargs_repr)           
        if signature: print(f"{'|   ' * (level)}\n{'|   ' * (level)}> {func.__name__} called with:\n{signature}")
        else: print(f"{'|   ' * (level)}\n{'|   ' * (level)}> {func.__name__} called")
        level += 1
        value = func(*args, **kwargs)
        level -= 1
        if len(repr(value)) < 100: print(f"{'|   ' * (level + 1)}\n{'|   ' * (level)}< {func.__name__!r} returned {value!r}")
        else: print(f"{'|   ' * (level + 1)}\n{'|   ' * (level)}< {func.__name__!r} returned {repr(value)[:98]}...")
        return value
    return wrapper_debug