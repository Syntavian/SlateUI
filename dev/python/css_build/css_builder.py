
import re

from python.debug import debug
from python.utils.string_utils import *


@debug
def build_css(_slate_css_dir: str, _css_in_dir: str, _css_out_dir: str, _style_selectors: set[str]) -> None:
    input_css_file = open(f"{_slate_css_dir}/slate.css", "r")
    output_css_file_text = ""

    keyframes_blocks = {}
    media_blocks = {}

    is_in_required_block = False

    is_in_keyframes_block = False
    current_keyframes_block = ""

    is_in_media_block = False
    current_media_block = ""

    block_level = 0
    active_block_level = 0

    for input_css_file_line in input_css_file.readlines():
        line = input_css_file_line.strip()
        if len(line) > 0 and line[-1] == r'{':
            matches = set([(a.group(1), a.group(2)) for a in re.finditer(
                r"(?:[\.# ]?([a-zA-Z][\w-]*?)[ ,.#:>+])|^(\*) ", input_css_file_line)])
            if len(matches) > 0 and any((m[0] in _style_selectors or m[1] in _style_selectors) for m in matches):
                is_in_required_block = True
        if '@' in input_css_file_line:
            is_in_required_block = False
            active_block_level += 1
            if "keyframes" in input_css_file_line:
                is_in_keyframes_block = True
                current_keyframes_block = remove_whitespace(
                    input_css_file_line)
                if current_keyframes_block not in keyframes_blocks.keys():
                    keyframes_blocks[current_keyframes_block] = ''
            elif "media" in input_css_file_line:
                is_in_media_block = True
                current_media_block = remove_whitespace(input_css_file_line)
                if current_media_block not in media_blocks.keys():
                    media_blocks[current_media_block] = ''
            else:
                output_css_file_text = output_css_file_text + \
                    remove_whitespace(input_css_file_line)
        if ('{' in input_css_file_line):
            block_level += 1
        if is_in_media_block and is_in_required_block:
            media_blocks[current_media_block] = media_blocks[current_media_block] + \
                remove_whitespace(input_css_file_line)
        elif is_in_keyframes_block:
            keyframes_blocks[current_keyframes_block] = keyframes_blocks[current_keyframes_block] + \
                remove_whitespace(input_css_file_line)
        elif is_in_required_block:
            output_css_file_text = output_css_file_text + \
                remove_whitespace(input_css_file_line)
        if ('}' in input_css_file_line):
            block_level -= 1
            if block_level < active_block_level and not is_in_keyframes_block and not is_in_media_block:
                output_css_file_text = output_css_file_text + \
                    remove_whitespace(input_css_file_line)
            if block_level <= active_block_level:
                active_block_level = block_level
                is_in_required_block = False
            if block_level == 0:
                is_in_keyframes_block = False
                is_in_media_block = False

    for media_selector, media_block in media_blocks.items():
        output_css_file_text = output_css_file_text + media_selector + media_block + '} '

    for keyframes_block in keyframes_blocks.values():
        output_css_file_text = output_css_file_text + keyframes_block

    input_css_file.close()

    output_css_file_text = remove_symbol_spaces(output_css_file_text)

    output_css = open(_css_out_dir + "/slate.css", "w")
    output_css.write(output_css_file_text)
    output_css.close()
