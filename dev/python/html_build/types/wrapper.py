import re
from enum import Enum
from typing import Literal

from python.debug import debug
from python.html_build.types.tag import Tag
from python.utils.error_utils import exception


class WrapperType(Enum):
    INVALID = 0
    ALL = 1
    PAGE = 2
    COMPONENT = 3


@debug
def determine_wrapper_type(
    _wrapper: str,
) -> Literal[
    WrapperType.COMPONENT, WrapperType.PAGE, WrapperType.ALL, WrapperType.INVALID
]:
    """Return the type of a wrapper"""
    if re.search(r"\*@\w+", _wrapper):
        return WrapperType.COMPONENT
    if re.search(r"\*\w+", _wrapper):
        return WrapperType.PAGE
    if re.search(r"\* |\*$", _wrapper):
        return WrapperType.ALL
    exception()(f"wrapper {_wrapper} is not valid.")
    return WrapperType.INVALID


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
        tags = ""
        for tag in self.tags:
            tags += f"{tag}"
        tags = re.sub(r"\n", "\n\t", tags)
        return f"Wrapper<{self.type}, {self.wrapped_object}>\ntags:\n\t{tags}"
