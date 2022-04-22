from python.html_build.types.tag import Tag
from python.utils.console_utils import describe_class


class Component:
    """A HTML Component."""

    def __init__(self, _html: str, _tags: list[Tag]) -> None:
        self._html = _html
        self._tags = _tags

    @property
    def html(self) -> str:
        return self._html

    @property
    def tags(self) -> list[Tag]:
        return self._tags

    @html.setter
    def html(self, _new_html: str) -> None:
        self._html = _new_html

    @tags.setter
    def tags(self, _new_tags: list[Tag]) -> None:
        self._tags = _new_tags

    def __str__(self) -> str:
        return describe_class(
            "Component",
            html=self._html,
            tags=self._tags,
        )
