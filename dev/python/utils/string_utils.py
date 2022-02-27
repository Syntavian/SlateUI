import re

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
