from enum import Enum
from typing import Literal, Match

class WrapperType(Enum):
    INVALID   = 0
    ALL       = 1
    PAGE      = 2
    COMPONENT = 3

class Wrapper:
    """An HTML Wrapper component."""
    def __init__(
        self, 
        _type: Literal[WrapperType.COMPONENT, WrapperType.PAGE, WrapperType.ALL, WrapperType.INVALID], 
        _before: str, 
        _after: str, 
        _wrapped_object: str,
        _tag_matches: list[Match[str]]
    ) -> None:
        self.type = _type
        self.before = _before
        self.after = _after
        self.wrapped_object = _wrapped_object
        self.tag_matches = _tag_matches
