import re
from enum import Enum
from typing import Literal

from python.debug import debug
from python.html_build.types.tag import Tag
from python.utils.console_utils import describe_class
from python.utils.error_utils import exception


class WrapperType(Enum):
    INVALID = 0
    ROOT = 1
    PAGE = 2
    COMPONENT = 3


WrapperTypeMember = Literal[
    WrapperType.COMPONENT, WrapperType.PAGE, WrapperType.ROOT, WrapperType.INVALID
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
        return WrapperType.ROOT
    exception()(f"wrapper {_wrapper} is not valid.")
    return WrapperType.INVALID


class Wrapper:
    """A HTML Wrapper component."""

    def __init__(
        self,
        _type: WrapperTypeMember,
        _html: str,
        _wrapper_tag: Tag,
        _wrapped_object: str,
        _tags: list[Tag],
    ) -> None:
        self._type = _type
        self._html = _html
        self._wrapper_tag = _wrapper_tag
        self._wrapped_object = _wrapped_object
        self._tags = _tags

    @property
    def type(self) -> WrapperTypeMember:
        return self._type

    @property
    def html(self) -> str:
        return self._html

    @property
    def wrapper_tag(self) -> Tag:
        return self._wrapper_tag

    @property
    def wrapped_object(self) -> str:
        return self._wrapped_object

    @property
    def tags(self) -> list[Tag]:
        return self._tags

    def __str__(self) -> str:
        return describe_class(
            "Wrapper",
            type=self._type,
            html=self._html,
            wrapper_tag=self._wrapper_tag,
            wrapped_object=self._wrapped_object,
            tags=self._tags,
        )


class ComputedWrapper:
    """A HTML Wrapper component's computed HTML content."""

    def __init__(
        self,
        _before: str,
        _after: str,
    ) -> None:
        self._before = _before
        self._after = _after

    @property
    def before(self) -> str:
        return self._before

    @property
    def after(self) -> str:
        return self._after

    def __str__(self) -> str:
        return describe_class(
            "ComputedWrapper",
            before=self._before,
            after=self._after,
        )
