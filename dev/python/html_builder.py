from enum import Enum
import os
import re
from typing import Any, Literal
from python.html_templating import *
from python.file_utils import *

class WrapperType(Enum):
    INVALID   = 0
    ALL       = 1
    PAGE      = 2
    COMPONENT = 3

class Wrapper:
    def __init__(self, type, before, after, wrapped_object):
        self.type = type
        self.before = before
        self.after = after
        self.wrapped_object = wrapped_object

def within_slate(_regex: str) -> str:
    return f"<!--#.*?({_regex}).*?#-->"

def find_string_values(_text: str) -> list[str | Any]:
    matches = re.finditer(within_slate(r"(?:\".*?\")|(?:'.*?')"), _text)
    return [match.group(1) for match in matches]

def fast_check_wrapper(_html: str) -> bool:
    if re.search(within_slate('\*'), _html):
        return True
    return False

def find_wrappers(_html: str) -> list[str | Any]:
    wrapper_matches = re.finditer(within_slate(r"\*(?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$)\S*"), _html)
    return [match.group(1) for match in wrapper_matches]

def get_wrapper_type(_wrapper: str) -> Literal[WrapperType.COMPONENT, WrapperType.PAGE, WrapperType.ALL, WrapperType.INVALID]:
    if re.search(r"\*@\w+", _wrapper):
        return WrapperType.COMPONENT
    if re.search(r"\*\w+", _wrapper):
        return WrapperType.PAGE
    if re.search(r"\* |\*$", _wrapper):
        return WrapperType.ALL
    print(f"Error: wrapper {_wrapper} is invalid")
    return WrapperType.INVALID

def exit_invalid_root_wrapper():
    print("Error: root HTML wrapper is not valid.")
    exit()

def compute_wrapper(_html: str, _is_root: bool) -> Wrapper | None:
    # Find and validate the wrapper.
    wrapper_matches = find_wrappers(_html)

    if not wrapper_matches:
        if _is_root: exit_invalid_root_wrapper()
        return
    elif len(wrapper_matches) > 1:
        if _is_root: exit_invalid_root_wrapper()
        print("Error: multiple wrapper selectors are not valid.")
        return

    wrapper = wrapper_matches[0]
    wrapper_type = get_wrapper_type(wrapper)

    if _is_root and wrapper_type != WrapperType.ALL:
        exit_invalid_root_wrapper()

    type = WrapperType.ALL
    
    return

def build_html(_slate_dir, _html_in_dir, _html_out_dir):
    # variableName: value
    global_variables: dict[str, str] = {}
    # wrappedObject: [{ 'before': HTML, 'after': HTML }]
    wrappers: dict[str, list[Wrapper]] = {}
    # Get the root HTML wrapper from slate.html.
    with open(f"{_slate_dir}/slate.html", "r") as root_html:
        root = root_html.read() 
        if not fast_check_wrapper(root):
            exit_invalid_root_wrapper()
        wrapper: Wrapper | None = compute_wrapper(root)
        if wrapper:
            if not wrappers[wrapper.wrapped_object]:
                wrappers[wrapper.wrapped_object] = []
            wrappers[wrapper.wrapped_object].append(wrapper)    

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
