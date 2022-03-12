from enum import Enum


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
