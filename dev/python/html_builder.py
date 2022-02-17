from enum import Enum
import os
import re
from textwrap import wrap
from python.html_templating import *
from python.file_utils import *

class Wrapper(Enum):
    INVALID   = 0
    ALL       = 1
    PAGE      = 2
    COMPONENT = 3

def within_slate(_regex):
    return f"<!--#.*?({_regex}).*?#-->"

def find_string_values(_text):
    matches = re.finditer(within_slate(r"(?:\".*?\")|(?:'.*?')"), _text)
    return [match.group(1) for match in matches]

def find_wrappers(_html):
    wrapper_matches = re.finditer(within_slate(r"\*(?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$)\S*"), _html)
    return [match.group(1) for match in wrapper_matches]

def get_wrapper_type(_wrapper):
    if re.search(r"\*@\w+", _wrapper):
        return Wrapper.COMPONENT
    if re.search(r"\*\w+", _wrapper):
        return Wrapper.PAGE
    if re.search(r"\* |\*$", _wrapper):
        return Wrapper.ALL
    print(f"Error: wrapper {_wrapper} is invalid")
    return Wrapper.INVALID

def compute_wrapper(_wrappers_ref, _html):
    pass

def build_html(_slate_dir, _html_in_dir, _html_out_dir):
    # variableName: value
    global_variables = {}
    # wrappedObject: { before: HTML, after: HTML }
    wrappers = {}
    root = ""
    with open(f"{_slate_dir}/slate.html", "r") as root_html:
        root = root_html.read() 

        # Find the wrapper
        wrapper_matches = find_wrappers(root)

        print(wrapper_matches)

        for match in wrapper_matches:
            print(match)
            print(get_wrapper_type(match))

        if not wrapper_matches or len(wrapper_matches) > 1 or get_wrapper_type(wrapper_matches[0]) != Wrapper.ALL:
            print("Error: root HTML is not a valid wrapper.")
            exit()

    print("root", '\n', root)

    string_matches = find_string_values(root)

    for match in string_matches:
        print(match)

    exit()

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
