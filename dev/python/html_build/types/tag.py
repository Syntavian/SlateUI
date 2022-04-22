from python.html_build.types.argument import Argument
from python.utils.console_utils import describe_class


class Tag:
    """A Slate tag holding a position and arguments"""

    def __init__(
        self, _position: int, _length: int, _text: str, _arguments: list[Argument]
    ) -> None:
        self._position = _position
        self._length = _length
        self._text = _text
        self._arguments = _arguments

    @property
    def position(self) -> int:
        return self._position

    @property
    def length(self) -> int:
        return self._length

    @property
    def text(self) -> str:
        return self._text

    @property
    def arguments(self) -> list[Argument]:
        return self._arguments

    @position.setter
    def position(self, _new_position: int) -> None:
        self._position = _new_position

    @length.setter
    def length(self, _new_length: int) -> None:
        self._length = _new_length

    @text.setter
    def text(self, _new_text: str) -> None:
        self._text = _new_text

    @arguments.setter
    def arguments(self, _new_arguments: list[Argument]) -> None:
        self._arguments = _new_arguments

    def __str__(self):
        return describe_class(
            "Tag",
            position=self._position,
            length=self._length,
            arguments=self._arguments,
        )
