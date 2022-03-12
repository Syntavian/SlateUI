import os
import re
from python.debug import debug

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


@debug
def find_required_styles(_html_path: str) -> set[str]:
    # A set of id and class selectors that must be built.
    style_selectors = set(REQUIRED_STYLES)
    # Analyse HTML files for tags, ids, and classes.
    for (dir_path, dir_names, file_names) in os.walk(_html_path):
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
    return style_selectors
