from typing import Match

class Page:
    def __init__(self, _path: str, _html: str, _tag_matches: list[Match[str]]) -> None:
        self.path = _path
        self.html = _html
        self.tag_matches = _tag_matches

    def __str__(self) -> str:
        return f"Page<{self.path}>"
