from python.html_build.types.argument import Argument


class Tag:
    """A Slate tag holding a position and arguments"""

    def __init__(self, _position: int, _length: int, _arguments: list[Argument]) -> None:
        self.position = _position
        self.length = _length
        self.arguments = _arguments
