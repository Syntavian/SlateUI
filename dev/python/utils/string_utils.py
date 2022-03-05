import re
from typing import Any, Iterable
from python.utils.function_utils import repeat_function

def redact_spacing(text: str) -> str:
    return re.sub(r"\s+", ' ', text)

def redact_overflow(_text: str, _max_length: int = 100) -> str:
    if len(_text) > _max_length:
        return f"{_text[:98]}..."
    else:
        return _text

def repeat(_text: str, _times: int, _separator: str = '\n', _end: str = '') -> str:
    return f"{_text}{_separator}" * (_times - 1) + f"{_text}" + _end

def repeat_string_function(_function, _times: int, _args: Iterable[Iterable] = [], _separator: str = '\n', _end: str = '') -> str:
    return _separator.join(repeat_function(_function, _times, _args)) + _end

def format_value(_value: Any):
    return redact_overflow(redact_spacing(str(_value)))

def substitute_quotes_whitespace(_string: str, _substitution: str = "!/~/#/") -> str:
    result = ""
    index = 0
    last_index = 0
    for match in re.finditer(r'".*?"|\'.*?\'|`.*?`|@media.*?{|calc\(.*?\)', _string):
        if ' ' in match.group(0):
            index = match.start()
            result = result + _string[last_index:index] + match.group(0).replace(' ', _substitution)
            last_index= match.end()
    result = result + _string[last_index:]
    return result

def remove_whitespace(_string: str, _separator: str = ' ') -> str:
    modified_string = substitute_quotes_whitespace(_string)
    result = _separator.join(modified_string.replace('\n', _separator).replace('\r', _separator).replace('\t', _separator).replace('\t', _separator).replace('\v', _separator).replace('\f', _separator).split())
    if "!/~/#/" in result:
        result = result.replace("!/~/#/", ' ')
    return result

def remove_symbol_spaces(_string: str) -> str:
    modified_string = substitute_quotes_whitespace(_string, "?/~/#/")
    result = ""
    last_index = 0
    for match in re.finditer(r' *[^\w ] *', modified_string):
        index = match.start()
        result = result + modified_string[last_index:index] + remove_whitespace(match.group(0), '')
        last_index = match.end()
    result = result + modified_string[last_index:]
    if "?/~/#/" in result:
        result = result.replace("?/~/#/", ' ')
    return result
