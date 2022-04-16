from enum import Enum
from typing import Literal


class ArgumentType(Enum):
    INVALID = 0
    VARIABLE_ASSIGNMENT = 1
    GLOBAL_ASSIGNMENT = 2
    VARIABLE = 3
    GLOBAL = 4
    ROOT_WRAPPER = 5
    PAGE_WRAPPER = 6
    COMPONENT_WRAPPER = 7
    COMPONENT = 8
    PAGE = 9


class Argument:
    def __init__(
        self,
        _value: str,
        _type: Literal[
            ArgumentType.VARIABLE_ASSIGNMENT,
            ArgumentType.GLOBAL_ASSIGNMENT,
            ArgumentType.INVALID,
            ArgumentType.ROOT_WRAPPER,
            ArgumentType.COMPONENT_WRAPPER,
            ArgumentType.PAGE_WRAPPER,
            ArgumentType.VARIABLE,
            ArgumentType.GLOBAL,
            ArgumentType.COMPONENT,
            ArgumentType.PAGE,
        ],
    ) -> None:
        self.value = _value
        self.type = _type

    def __str__(self):
        return f"\tvalue: {self.value}\n\ttype: {self.type}\n"
