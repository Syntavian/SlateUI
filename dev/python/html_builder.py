import os
from python.html_templating import *

def build_html(_html_in_dir, _html_out_dir):
    # Build HTML
    print("Compiling Slate HTML...")
    templates = {}

    for (dirpath, dirnames, filenames) in os.walk(_html_in_dir + "/components"):
        for template_file_name in filenames:
            template_file = open(dirpath + "\\" + template_file_name, "r")
            template_file_name_text = os.path.splitext(template_file_name)[0]
            templates[template_file_name_text] = ""
            for line in template_file.readlines():
                templates[template_file_name_text] = templates[template_file_name_text] + line
            template_file.close()

    PAGES_DIR = _html_in_dir + "/pages"

    for (dirpath, dirnames, filenames) in os.walk(PAGES_DIR):
        sub_dir = ""

        if dirpath != PAGES_DIR:
            sub_dir = dirpath.replace(PAGES_DIR, "")
        for page_file_name in filenames:
            page_file = open(dirpath + "\\" + page_file_name, "r")
            page_file_text = ""

            for page_file_line in page_file.readlines():
                page_file_text = page_file_text + page_file_line
            page_file.close()

            variables = {}
            current_page_result = process_text(page_file_text, variables, templates)

            output_file = open(_html_out_dir + sub_dir + "\\" + page_file_name, "w")
            output_file.write(current_page_result)
            output_file.close()
