from enum import Enum
from typing import Literal

from python.html_build.types.tag import Tag


class WrapperType(Enum):
    INVALID = 0
    ALL = 1
    PAGE = 2
    COMPONENT = 3


class Wrapper:
    """An HTML Wrapper component."""

    def __init__(
        self,
        _type: Literal[
            WrapperType.COMPONENT,
            WrapperType.PAGE,
            WrapperType.ALL,
            WrapperType.INVALID,
        ],
        _before: str,
        _after: str,
        _wrapped_object: str,
        _tags: list[Tag],
    ) -> None:
        self.type = _type
        self.before = _before
        self.after = _after
        self.wrapped_object = _wrapped_object
        self.tags = _tags

    def __str__(self) -> str:
        return f"Wrapper<{self.type}, {self.wrapped_object}>"
