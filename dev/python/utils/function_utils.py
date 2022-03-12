from typing import Iterable


def repeat_function(_function, _times: int, _args: Iterable[Iterable] = []) -> list:
    return [_function(*(_args[i])) for i in range(_times)]
