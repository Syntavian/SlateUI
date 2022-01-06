import os
import re

HTML_DIR = "./build"
SLATE_DIR = "./build/css"
OUTPUT_DIR = "./build/compile"

if __name__ == "__main__":
    for (dirpath, dirnames, filenames) in os.walk(HTML_DIR):
        sub_dir = ""

        if dirpath != HTML_DIR:
            sub_dir = dirpath.replace(HTML_DIR, "")
        for html_file_name in [filename for filename in filenames if os.path.splitext(filename)[1] == ".html"]:
            html = open(dirpath + "\\" + html_file_name, "r")
            print(f"\nWorking on {html_file_name}\n")
            page_file_text = ""

            for page_file_line in html.readlines():
                page_file_text = page_file_text + page_file_line
            html.close()

            print(page_file_text)
            
            styleClassIndices = (styleClassIndex.start() for styleClassIndex in re.finditer("class=", page_file_text))
            styleClasses = set()

            for styleClassIndex in styleClassIndices:
                for styleClass in page_file_text[styleClassIndex + 7 : page_file_text.find('"', styleClassIndex + 7)].split():
                    styleClasses.add(styleClass)

            for sc in styleClasses:
                print(sc)
