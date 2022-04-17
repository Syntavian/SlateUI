from enum import Enum
from typing import Literal

from python.debug import debug


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


@debug
def determine_argument_type(
    _argument: str,
) -> Literal[
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
]:
    """Return the Argument type of _argument based on the identifier and whether it is an assignment"""
    if "=" in _argument:
        if _argument[0] == "$":
            return ArgumentType.VARIABLE_ASSIGNMENT
        elif _argument[0] == "%":
            return ArgumentType.GLOBAL_ASSIGNMENT
        else:
            return ArgumentType.INVALID
    elif _argument[0] == "*":
        if len(_argument) == 1:
            return ArgumentType.ROOT_WRAPPER
        elif _argument[1] == "@":
            return ArgumentType.COMPONENT_WRAPPER
        else:
            return ArgumentType.PAGE_WRAPPER
    elif _argument[0] == "$":
        return ArgumentType.VARIABLE
    elif _argument[0] == "%":
        return ArgumentType.GLOBAL
    elif _argument[0] == "@":
        return ArgumentType.COMPONENT
    else:
        return ArgumentType.PAGE


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
