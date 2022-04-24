from python.html_build.types.component import Component
from python.html_build.types.tag import Tag
from python.utils.console_utils import describe_class


class Page(Component):
    def __init__(self, _path: str, _html: str, _tags: list[Tag]) -> None:
        super().__init__(_html, _tags)
        self._path = _path

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, _new_path: str) -> None:
        self._path = _new_path

    def __str__(self) -> str:
        return describe_class("Page", path=self._path, html=self._html, tags=self._tags)
