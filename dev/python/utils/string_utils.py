import re

def substitute_quotes_whitespace(string: str, substitution: str = "!/~/#/"):
    result = ""
    index = 0
    last_index = 0
    for match in re.finditer(r'".*?"|\'.*?\'|`.*?`|@media.*?{|calc\(.*?\)', string):
        if ' ' in match.group(0):
            index = match.start()
            result = result + string[last_index:index] + match.group(0).replace(' ', substitution)
            last_index= match.end()
    result = result + string[last_index:]
    return result

def remove_whitespace(string: str, separator: str = ' ', end: str = ' ') -> str:
    modified_string = substitute_quotes_whitespace(string)
    result = separator.join(modified_string.replace('\n', separator).replace('\r', separator).replace('\t', separator).replace('\t', separator).replace('\v', separator).replace('\f', separator).split())
    if "!/~/#/" in result:
        result = result.replace("!/~/#/", ' ')
    return result

def remove_symbol_spaces(string: str) -> str:
    modified_string = substitute_quotes_whitespace(string, "?/~/#/")
    result = ""
    last_index = 0
    for match in re.finditer(r' *[^\w ] *', modified_string):
        index = match.start()
        result = result + modified_string[last_index:index] + remove_whitespace(match.group(0), '', '')
        last_index = match.end()
    result = result + modified_string[last_index:]
    if "?/~/#/" in result:
        result = result.replace("?/~/#/", ' ')
    return result
