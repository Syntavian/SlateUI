import os
import re

HTML_DIR = "./build"
SLATE_CSS_DIR = "./scss_compiled"
SLATE_JS_DIR = "./js"
CSS_OUTPUT_DIR = "./build/css"
JS_OUTPUT_DIR = "./build/js"
JS_FILE_ORDER = [
    "utils.js",
    "button_styles.js",
    "image_styles.js",
    "sticky_styles.js",
    "scroll_styles.js",
    "layout_styles.js",
    "theme_styles.js",
]
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

if __name__ == "__main__":
    # A set of id and class selectors that must be compiled.
    style_selectors = set(REQUIRED_STYLES)

    # HTML
    # Analyse HTML files for tags, ids, and classes.
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

    # CSS
    # ...
    input_css = open(SLATE_CSS_DIR + "/style.css", "r")
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
                current_keyframes_block = remove_whitespace(input_css_file_line)
                if current_keyframes_block not in keyframes_blocks.keys():
                    keyframes_blocks[current_keyframes_block] = ''
            elif "media" in input_css_file_line:
                is_in_media_block = True
                current_media_block = remove_whitespace(input_css_file_line)
                if current_media_block not in media_blocks.keys():
                    media_blocks[current_media_block] = ''
            else:
                output_css_file_text = output_css_file_text + remove_whitespace(input_css_file_line)
        if ('{' in input_css_file_line):
            block_level += 1
        if is_in_media_block and is_in_required_block:
            media_blocks[current_media_block] = media_blocks[current_media_block] + remove_whitespace(input_css_file_line)
        elif is_in_keyframes_block:
            keyframes_blocks[current_keyframes_block] = keyframes_blocks[current_keyframes_block] + remove_whitespace(input_css_file_line)
        elif is_in_required_block:
            output_css_file_text = output_css_file_text + remove_whitespace(input_css_file_line)
        if ('}' in input_css_file_line):
            block_level -= 1
            if block_level < active_block_level and not is_in_keyframes_block and not is_in_media_block:
                output_css_file_text = output_css_file_text + remove_whitespace(input_css_file_line)
            if block_level <= active_block_level:
                active_block_level = block_level
                is_in_required_block = False
            if block_level == 0: 
                is_in_keyframes_block = False
                is_in_media_block = False

    for media_selector, media_block in media_blocks.items():
        output_css_file_text = output_css_file_text + media_selector + media_block + '} '

    for keyframes_selector, keyframes_block in keyframes_blocks.items():
        output_css_file_text = output_css_file_text + keyframes_block

    input_css.close()

    output_css_file_text = remove_symbol_spaces(output_css_file_text)

    output_css = open(CSS_OUTPUT_DIR + "/slate.css", "w")
    output_css.write(output_css_file_text)

    # JS
    # ...
    js_file_texts = {}

    for (dir_path, dir_names, file_names) in os.walk(SLATE_JS_DIR):
        sub_dir = ""

        if dir_path != SLATE_JS_DIR:
            sub_dir = dir_path.replace(SLATE_JS_DIR, "")
        for js_file_name in [filename for filename in file_names if os.path.splitext(filename)[1] == ".js"]:
            js_file = open(dir_path + "\\" + js_file_name, "r")
            js_file_texts[js_file_name] = ""

            for js_file_line in js_file.readlines():
                if "import" not in js_file_line and js_file_line != "\n" and js_file_line != "\r":
                    if "//" in js_file_line:
                        js_file_texts[js_file_name] = js_file_texts[js_file_name] + remove_whitespace(js_file_line.replace(js_file_line[js_file_line.find("//"):], ' ').replace("export", ' '))
                    else:
                        js_file_texts[js_file_name] = js_file_texts[js_file_name] + remove_whitespace(js_file_line.replace("export", ' '))
            js_file.close()

    output_js_file_text = ""

    for js_file_name in JS_FILE_ORDER:
        output_js_file_text = output_js_file_text + js_file_texts[js_file_name]

    output_js_file_text = remove_symbol_spaces(output_js_file_text)

    output_js = open(JS_OUTPUT_DIR + "/slate.js", "w")
    output_js.write(output_js_file_text)
