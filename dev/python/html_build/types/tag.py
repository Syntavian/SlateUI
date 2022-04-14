from python.html_build.types.argument import Argument


class Tag:
    """A Slate tag holding a position and arguments"""

    def __init__(self, _position: int, _length: int, _text: str, _arguments: list[Argument]) -> None:
        self.position = _position
        self.length = _length
        self.text = _text
        self.arguments = _arguments

    def __str__(self):
        arguments = ""
        for argument in self.arguments:
            arguments += f"\n\t{argument}"
        return f"position: {self.position}\nlength: {self.length}\narguments: {arguments}\n"
