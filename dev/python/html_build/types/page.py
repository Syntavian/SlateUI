from python.html_build.types.tag import Tag
from python.utils.console_utils import describe_class


class Page:
    def __init__(self, _path: str, _html: str, _tags: list[Tag]) -> None:
        self._path = _path
        self._html = _html
        self._tags = _tags

    def __str__(self) -> str:
        return describe_class("Page", path=self._path, html=self._html, tags=self._tags)
