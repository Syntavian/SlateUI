from enum import Enum
from typing import Literal

from python.debug import debug
from python.utils.console_utils import describe_class


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


ArgumentTypeMember = Literal[
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
]


@debug
def determine_argument_type(
    _argument: str,
) -> ArgumentTypeMember:
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
        _type: ArgumentTypeMember,
    ) -> None:
        self._value = _value
        self._type = _type

    @property
    def value(self) -> str:
        return self._value

    @property
    def type(self) -> ArgumentTypeMember:
        return self._type

    @value.setter
    def value(self, _new_value: str) -> None:
        self._value = _new_value

    @type.setter
    def type(self, _new_type: ArgumentTypeMember) -> None:
        self._type = _new_type

    def __str__(self):
        return describe_class("Argument", value=self._value, type=self._type)
