import os
from python.utils.string_utils import *

JS_FILE_ORDER = [
    "utils.js",
    "button_styles.js",
    "image_styles.js",
    "sticky_styles.js",
    "scroll_styles.js",
    "layout_styles.js",
    "theme_styles.js",
]

def build_js(_js_in_dir, _js_out_dir):
    js_file_texts = {}

    for (dir_path, dir_names, file_names) in os.walk(_js_in_dir):
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

    output_js = open(_js_out_dir + "/slate.js", "w")
    output_js.write(output_js_file_text)
    output_js.close()