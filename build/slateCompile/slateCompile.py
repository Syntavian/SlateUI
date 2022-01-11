import os
import re

HTML_DIR = "./build"
SLATE_DIR = "./build/css"
OUTPUT_DIR = "./build/compile"
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

if __name__ == "__main__":

    # A set of both id and class selectors that must be compiled
    styleSelectors = set(JS_REQUIRED_SELECTORS)

    # Analyse HTML files for style ids and classes
    for (dirpath, dirnames, filenames) in os.walk(HTML_DIR):
        sub_dir = ""

        if dirpath != HTML_DIR:
            sub_dir = dirpath.replace(HTML_DIR, "")
        for html_file_name in [filename for filename in filenames if os.path.splitext(filename)[1] == ".html"]:
            html_file = open(dirpath + "\\" + html_file_name, "r")
            html_file_text = ""

            for html_file_line in html_file.readlines():
                html_file_text = html_file_text + html_file_line
            html_file.close()

            for tags in [styleClassIndex.group(1).split() for styleClassIndex in re.finditer(r'<(\w+?)[ />]', html_file_text)]:  
                for tag in tags:
                    styleSelectors.add(tag)

            for tag_styles in [styleClassIndex.group(1).split() for styleClassIndex in re.finditer(r'(?:class|id)="(.+?)"', html_file_text)]:  
                for style in tag_styles:
                    styleSelectors.add(style)

    input_css = open(SLATE_DIR + "/style.css", "r")
    output_css_file_text = ""

    isInRequiredBlock = False
    isInKeyframesBlock = True
    blockLevel = 0
    activeBlockLevel = 0

    for input_css_file_line in input_css.readlines():
        line = input_css_file_line.strip()
        if len(line) > 0 and line[-1] == r'{':
            matches = set([a.group(1) for a in  re.finditer(r"(?:[\.# ]?([a-zA-Z][\w-]*?)[ ,.#:>+])", input_css_file_line)])
            if len(matches) > 0 and any((m in styleSelectors) for m in matches):
                isInRequiredBlock = True
        if '@' in input_css_file_line:
            isInRequiredBlock = False
            activeBlockLevel += 1
            if 'keyframes' in input_css_file_line:
                isInKeyframesBlock = True
            else:
                output_css_file_text = output_css_file_text + input_css_file_line
        if ('{' in input_css_file_line):
            blockLevel += 1
        if isInRequiredBlock or isInKeyframesBlock:
            output_css_file_text = output_css_file_text + input_css_file_line
        if ('}' in input_css_file_line):
            blockLevel -= 1
            if blockLevel < activeBlockLevel and not isInKeyframesBlock:
                output_css_file_text = output_css_file_text + input_css_file_line
            if blockLevel <= activeBlockLevel:
                activeBlockLevel = blockLevel
                isInRequiredBlock = False
            if blockLevel == 0: 
                isInKeyframesBlock = False

    input_css.close()

    output_css = open(OUTPUT_DIR + "/style.css", "w")
    output_css.write(output_css_file_text)
