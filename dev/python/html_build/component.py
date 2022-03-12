from typing import Match


class Component:
    """An HTML Component."""

    def __init__(self, _html: str, _tag_matches: list[Match[str]]) -> None:
        self.html = _html
        self.tag_matches = _tag_matches

    def __str__(self) -> str:
        if len(self.html) <= 20:
            return f"Component<{self.html}>"
        return f"Component<{self.html[:10]}...{self.html[-10:]}>"
