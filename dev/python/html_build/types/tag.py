from python.html_build.types.argument import Argument
from python.utils.console_utils import describe


class Tag:
    """A Slate tag holding a position and arguments"""

    def __init__(
        self, _position: int, _length: int, _text: str, _arguments: list[Argument]
    ) -> None:
        self.position = _position
        self.length = _length
        self.text = _text
        self.arguments = _arguments

    def __str__(self):
        return describe(
            "Tag", position=self.position, length=self.length, arguments=self.arguments
        )
