import re
from enum import Enum
from typing import Literal

from python.debug import debug
from python.html_build.types.tag import Tag
from python.utils.console_utils import describe
from python.utils.error_utils import exception


class WrapperType(Enum):
    INVALID = 0
    ALL = 1
    PAGE = 2
    COMPONENT = 3


WrapperTypeMember = Literal[
    WrapperType.COMPONENT, WrapperType.PAGE, WrapperType.ALL, WrapperType.INVALID
]


@debug
def determine_wrapper_type(
    _wrapper: str,
) -> WrapperTypeMember:
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
        _type: WrapperTypeMember,
        _before: str,
        _after: str,
        _wrapped_object: str,
        _tags: list[Tag],
    ) -> None:
        self._type = _type
        self._before = _before
        self._after = _after
        self._wrapped_object = _wrapped_object
        self._tags = _tags

    def __str__(self) -> str:
        return describe(
            "Wrapper",
            type=self._type,
            before=self._before,
            after=self._after,
            wrapped_object=self._wrapped_object,
            tags=self._tags,
        )
