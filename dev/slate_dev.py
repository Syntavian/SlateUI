import os
import re
import subprocess
import time
from watchdog.observers import Observer
from python.string_utils import *

from python.thread_handler import ThreadHandler
from python.compile_event_handler import ModifiedEventCompileEventHandler

SLATE_HTML_DIR = "./build/html"
SLATE_CSS_DIR = "./dev/css"
SLATE_JS_DIR = "./dev/js"
BUILD_SLATE_CSS_DIR = "./build/slate_ui"
HTML_OUTPUT_DIR = "./build/app/public"
SLATE_CSS_OUTPUT_DIR = "./build/app/public/css"
JS_OUTPUT_DIR = "./build/app/public/js"

def recompile():

    # CSS
    # ...
    print("Transfering Slate CSS...")

    dev_css_file = open(SLATE_CSS_DIR + "/style.css", "r")
    dev_css = dev_css_file.read()
    dev_css_file.close()

    build_css_file = open(BUILD_SLATE_CSS_DIR + "/style.css", "w")
    build_css_file.write(dev_css)
    build_css_file.close()

    #...
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

if __name__ == "__main__":
    thread_handler = ThreadHandler(recompile)
    subprocess.Popen(["sass", "--watch", "dev\scss:dev\css"])
    time.sleep(1)
    recompile()
    event_handler = ModifiedEventCompileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, SLATE_CSS_DIR)
    observer.schedule(event_handler, SLATE_JS_DIR)
    observer.schedule(event_handler, SLATE_HTML_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
            event_handler.update(thread_handler)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    exit()
