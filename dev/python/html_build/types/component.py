import re

from python.html_build.types.tag import Tag


class Component:
    """An HTML Component."""

    def __init__(self, _html: str, _tags: list[Tag]) -> None:
        self.html = _html
        self.tags = _tags

    def __str__(self) -> str:
        html = re.sub(r"\s", " ", self.html)
        tags = ""
        for tag in self.tags:
            tags += f"{tag}"
        tags = re.sub(r"\n", "\n\t", tags)
        if len(html) <= 20:
            return f"Component<{html}>\n{tags}"
        return f"Component<{html[:10]}...{html[-10:]}>\ntags:\n\t{tags}"
