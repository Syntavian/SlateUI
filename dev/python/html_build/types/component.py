from python.utils.console_utils import describe
from python.html_build.types.tag import Tag


class Component:
    """A HTML Component."""

    def __init__(self, _html: str, _tags: list[Tag]) -> None:
        self._html = _html
        self._tags = _tags

    def __str__(self) -> str:
        return describe(
            "Component",
            html=self._html,
            tags=self._tags,
        )
