import os
import re

HTML_DIR = "./build"
SLATE_DIR = "./build/css"
OUTPUT_DIR = "./build/compile"

if __name__ == "__main__":

    # A set of both id and class selectors that must be compiled
    styleSelectors = set()

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

            styleSelectorIndices = (styleClassIndex.start() for styleClassIndex in re.finditer(r"class=|id=", html_file_text))

            for styleSelectorIndex in styleSelectorIndices:
                for styleSelector in html_file_text[styleSelectorIndex + 7 : html_file_text.find('"', styleSelectorIndex + 7)].split():
                    styleSelectors.add(styleSelector)

    input_css = open(SLATE_DIR + "/style.css", "r")
    output_css_file_text = ""

    isInRequiredBlock = False
    blockLevel = 0
    activeBlockLevel = 0

    for input_css_file_line in input_css.readlines():
        if blockLevel == activeBlockLevel and (any([(styleSelector in input_css_file_line) for styleSelector in styleSelectors])):
            isInRequiredBlock = True
        if '@' in input_css_file_line:
            isInRequiredBlock = False
            activeBlockLevel += 1
            if 'keyframes' in input_css_file_line:
                isInRequiredBlock = True
            else:
                output_css_file_text = output_css_file_text + input_css_file_line
        if ('{' in input_css_file_line):
            blockLevel += 1
        if isInRequiredBlock:
            output_css_file_text = output_css_file_text + input_css_file_line
        if ('}' in input_css_file_line):
            blockLevel -= 1
            if blockLevel < activeBlockLevel:
                output_css_file_text = output_css_file_text + input_css_file_line
            if blockLevel <= activeBlockLevel:
                activeBlockLevel = blockLevel
                isInRequiredBlock = False

    input_css.close()

    output_css = open(OUTPUT_DIR + "/style.css", "w")
    output_css.write(output_css_file_text)
