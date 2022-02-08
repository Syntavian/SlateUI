from directories import *
from html_builder import build_html
from css_builder import build_css
from js_builder import build_js
from find_required_styles import find_required_styles
from transfer_file import transfer

def build(path = "./"):
    # Create working HTML in public dir from HTML templates in src.
    build_html(path + HTML_DIR, path + HTML_OUT_DIR)
    # Transfer the SCSS output in dev to slate.css in build. @SLATE_OMIT_NEXT_LINE
    transfer(CSS_PREBUILD_DIR + "/style.css", SLATE_CSS_DIR + "/slate.css")
    # From the built HTML in public determine the required styles to build into optimised CSS.
    style_selectors = find_required_styles(path + HTML_OUT_DIR)
    # Create the public app CSS using the discovered CSS selectors.
    build_css((SLATE_CSS_DIR, BUILD_CSS_DIR), path + CSS_OUT_DIR, style_selectors)
    # TODO: run Babel for Slate JS before transfer (dev/js/src --> dev/js/lib).
    # Optimise and transfer Slate JS to build public. @SLATE_OMIT_NEXT_LINE
    build_js(path + JS_DIR, path + JS_OUT_DIR)

######################
#                    #
#   Refactor below   #
#                    #
######################

exit()

print("Compiling Slate CSS...")
input_css_file = open(BUILD_SLATE_CSS_DIR + "/style.css", "r")
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

for keyframes_block in keyframes_blocks.values():
    output_css_file_text = output_css_file_text + keyframes_block

input_css_file.close()

output_css_file_text = remove_symbol_spaces(output_css_file_text)

output_css = open(SLATE_CSS_OUTPUT_DIR + "/slate.css", "w")
output_css.write(output_css_file_text)
output_css.close()

# JS
# ...
print("Compiling Slate JS...")
js_file_texts = {}

for (dir_path, dir_names, file_names) in os.walk(SLATE_JS_DIR):
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
output_js.close()
print("Done\n")
