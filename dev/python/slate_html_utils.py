import re
from typing import Iterator, Match, Any

def containing(_regex: str) -> str:
    """Return a Regex wrapper for matching a whole string containing a subsection."""
    return f"((?:.|\s)*(?:{_regex})(?:.|\s)*)"

def find_string_values(_text: str) -> list[str | Any]:
    """Return a Match for every substring wrapped in quotes."""
    matches = re.finditer(r"((?:\".*?\")|(?:'.*?'))", _text)
    return [match.group(1) for match in matches]

def slate_tag() -> str:
    """Return a Slate HTML tag matcher."""
    return f"((?:<#(?:.|\s)*?\/>)|(?:<!--#(?:.|\s)*?\/-->))"

def strip_slate_tag(_slate_tag: str) -> str:
    """Return the contents of a Slate HTML tag."""
    match = re.search(r"(?:<#((?:.|\s)*?)\/>)|(?:<!--#((?:.|\s)*?)\/-->)", _slate_tag)
    if match.group(1):
        return match.group(1)
    return match.group(2)

def get_slate_tags(_html: str) -> Iterator[Match[str]]:
    """Return every match of a Slate tag within the provided HTML."""
    matches = re.finditer(slate_tag(), _html)
    return [match for match in matches]
