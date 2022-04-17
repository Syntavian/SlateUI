from python.html_build.types.tag import Tag


class Page:
    def __init__(self, _path: str, _html: str, _tags: list[Tag]) -> None:
        self.path = _path
        self.html = _html
        self.tags = _tags

    def __str__(self) -> str:
        return f"Page<{self.path}>"
