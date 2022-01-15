import os
import re

HTML_DIR = "./build"
SLATE_DIR = "./scss_compiled"
OUTPUT_DIR = "./build/css"
CSS_REQUIRED_SELECTORS = [
    "*",
]
JS_REQUIRED_SELECTORS = [
    "sticky",
    "div",
    "sticky-placeholder",
    "theme-selector",
    "select",
    "span",
    "option",
    "active",
    "inactive",
    "placeholder",
    "button",
    "fill",
    "disabled",
    "image",
    "image-carousel",
    "scroll-bar",
    "scroll-handle",
]
REQUIRED_STYLES = []
REQUIRED_STYLES.extend(CSS_REQUIRED_SELECTORS)
REQUIRED_STYLES.extend(JS_REQUIRED_SELECTORS)

if __name__ == "__main__":

    # A set of both id and class selectors that must be compiled
    style_selectors = set(REQUIRED_STYLES)

    # Analyse HTML files for style ids and classes
    for (dir_path, dir_names, file_names) in os.walk(HTML_DIR):
        sub_dir = ""

        if dir_path != HTML_DIR:
            sub_dir = dir_path.replace(HTML_DIR, "")
        for html_file_name in [filename for filename in file_names if os.path.splitext(filename)[1] == ".html"]:
            html_file = open(dir_path + "\\" + html_file_name, "r")
            html_file_text = ""

            for html_file_line in html_file.readlines():
                html_file_text = html_file_text + html_file_line
            html_file.close()

            for tags in [styleClassIndex.group(1).split() for styleClassIndex in re.finditer(r'<(\w+?)[ />]', html_file_text)]:  
                for tag in tags:
                    style_selectors.add(tag)

            for tag_styles in [styleClassIndex.group(1).split() for styleClassIndex in re.finditer(r'(?:class|id)="(.+?)"', html_file_text)]:  
                for style in tag_styles:
                    style_selectors.add(style)

    input_css = open(SLATE_DIR + "/style.css", "r")
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

    for input_css_file_line in input_css.readlines():
        line = input_css_file_line.strip()
        if len(line) > 0 and line[-1] == r'{':
            matches = set([(a.group(1), a.group(2)) for a in  re.finditer(r"(?:[\.# ]?([a-zA-Z][\w-]*?)[ ,.#:>+])|^(\*) ", input_css_file_line)])
            if len(matches) > 0 and any((m[0] in style_selectors or m[1] in style_selectors) for m in matches):
                is_in_required_block = True
        if '@' in input_css_file_line:
            is_in_required_block = False
            active_block_level += 1
            if "keyframes" in input_css_file_line:
                is_in_keyframes_block = True
                current_keyframes_block = input_css_file_line
                if current_keyframes_block not in keyframes_blocks.keys():
                    keyframes_blocks[current_keyframes_block] = ''
            elif "media" in input_css_file_line:
                is_in_media_block = True
                current_media_block = input_css_file_line
                if current_media_block not in media_blocks.keys():
                    media_blocks[current_media_block] = ''
            else:
                output_css_file_text = output_css_file_text + input_css_file_line
        if ('{' in input_css_file_line):
            block_level += 1
        if is_in_media_block and is_in_required_block:
            media_blocks[current_media_block] = media_blocks[current_media_block] + input_css_file_line
        elif is_in_keyframes_block:
            keyframes_blocks[current_keyframes_block] = keyframes_blocks[current_keyframes_block] + input_css_file_line
        elif is_in_required_block:
            output_css_file_text = output_css_file_text + input_css_file_line
        if ('}' in input_css_file_line):
            block_level -= 1
            if block_level < active_block_level and not is_in_keyframes_block and not is_in_media_block:
                output_css_file_text = output_css_file_text + input_css_file_line
            if block_level <= active_block_level:
                active_block_level = block_level
                is_in_required_block = False
            if block_level == 0: 
                is_in_keyframes_block = False
                is_in_media_block = False

    for media_selector, media_block in media_blocks.items():
        output_css_file_text = output_css_file_text + media_selector + media_block + '}\n'

    for keyframes_selector, keyframes_block in keyframes_blocks.items():
        output_css_file_text = output_css_file_text + keyframes_block

    input_css.close()

    output_css = open(OUTPUT_DIR + "/style.css", "w")
    output_css.write(output_css_file_text)
