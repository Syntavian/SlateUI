import os
from python.html_templating import *
from python.file_utils import *

def build_html(_slate_dir, _html_in_dir, _html_out_dir):
    global_variables = {}
    root = ""
    with open(f"{_slate_dir}/slate.html", "r") as root_html:
        root = root_html.read() 
    print("root", '\n', root)

    components = {}
    for dirpath, dirnames, filenames in os.walk(f"{_html_in_dir}/components"):
        for component_file_name in filenames:
            with open(dirpath + "\\" + component_file_name, "r") as component_file:
                component_file_name_text = get_file_name(component_file_name)
                components[f"@{component_file_name_text}"] = component_file.read() 
    for k, v in components.items():
        print(k, '\n', v)

    PAGES_DIR = _html_in_dir + "/pages"
    for dirpath, dirnames, filenames in os.walk(f"{PAGES_DIR}"):
        sub_dir = ""
        variables = {}
        if dirpath != PAGES_DIR:
            sub_dir = dirpath.replace(PAGES_DIR, "")
        for page_file_name in filenames:
            with open(dirpath + "\\" + page_file_name, "r") as page_file:
                page_file_text = page_file.read()
            current_page_result = process_text(page_file_text, variables, components)
            with open(_html_out_dir + sub_dir + "\\" + page_file_name, "w") as output_file:
                output_file.write(current_page_result)
