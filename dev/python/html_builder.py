import os
import re
from typing import Iterator, Literal, Match
from dev.python.component import *
from dev.python.error_utils import *
from dev.python.wrapper import *
from python.html_templating import *
from python.file_utils import *
from python.slate_html_utils import *

def fast_check_wrapper(_html: str) -> bool:
    if re.search(containing('\*'), _html):
        return True
    return False

def get_wrapper(_slate_tag_content: str) -> Match[str]:
    wrapper_matches = [wrapper_match for wrapper_match in re.finditer(containing(r"\*(?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$)\S*"), strip_slate_tag(_slate_tag_content))] 
    if not wrapper_matches:
        return
    elif len(wrapper_matches) > 1:
        exception("Multiple wrappers found.")
        return
    return wrapper_matches[0]

def get_wrapper_type(_wrapper: str) -> Literal[WrapperType.COMPONENT, WrapperType.PAGE, WrapperType.ALL, WrapperType.INVALID]:
    if re.search(r"\*@\w+", _wrapper):
        return WrapperType.COMPONENT
    if re.search(r"\*\w+", _wrapper):
        return WrapperType.PAGE
    if re.search(r"\* |\*$", _wrapper):
        return WrapperType.ALL
    exception(f"wrapper {_wrapper} is not valid.")
    return WrapperType.INVALID

def build_wrapper(_html: str, _slate_tag_match: Match[str], _slate_tag_matches: list[Match[str]], _is_root: bool = False) -> Wrapper | None:
    # Find and validate the wrapper.
    wrapper = get_wrapper(_slate_tag_match.group(1))
    if not wrapper: return None
    wrapper_type = get_wrapper_type(wrapper.group(1))
    if _is_root and wrapper_type != WrapperType.ALL:
        exit_exception("Root HTML wrapper is not valid.")
    if wrapper_type == WrapperType.INVALID:
        exception("Wrapper is not valid.")
        return
    return Wrapper(wrapper_type, _html[:_slate_tag_match.start()], _html[_slate_tag_match.end():], wrapper.group(1), _slate_tag_matches)

def handle_wrapper_build(_html: str, _slate_tag_matches: Iterator[Match[str]], _wrappers: dict[str, list[Wrapper]], _is_root: bool = False) -> bool:
    wrapper: Wrapper | None = None
    for slate_tag_match in _slate_tag_matches:
        if fast_check_wrapper(slate_tag_match.group(1)):
            newWrapper = build_wrapper(_html, slate_tag_match, _slate_tag_matches, _is_root)
            if newWrapper:
                if not wrapper:
                    wrapper = newWrapper
                else:
                    exit_exception("Multi-wrapper HTML is not valid.")
    if wrapper:
        if wrapper.wrapped_object not in _wrappers.keys(): _wrappers[wrapper.wrapped_object] = []
        _wrappers[wrapper.wrapped_object].append(wrapper) 
        return True
    return False

def build_html(_slate_dir, _html_in_dir, _html_out_dir) -> None:
    # Global variables store
    global_variables: dict[str, str] = {}
    # Component definitions
    components: dict[str, Component] = {}
    # Wrapper definitions
    wrappers: dict[str, list[Wrapper]] = {}
    # Get the root HTML wrapper from slate.html.
    with open(f"{_slate_dir}/slate.html", "r") as root_html_file:
        root_html = root_html_file.read() 
        slate_tag_matches = get_slate_tags(root_html)
        if not handle_wrapper_build(root_html, slate_tag_matches, wrappers, True):
            exit_exception("Root HTML wrapper is not valid.")

    for dirpath, dirnames, filenames in os.walk(f"{_html_in_dir}/components"):
        for component_file_name in filenames:
            with open(dirpath + "\\" + component_file_name, "r") as component_html_file:
                component_file_name_text = get_file_name(component_file_name)
                component_html = component_html_file.read()
                slate_tag_matches = [slate_tag_match for slate_tag_match in get_slate_tags(component_html)]
                if not handle_wrapper_build(component_html, slate_tag_matches, wrappers):
                    components[f"@{component_file_name_text}"] = Component(component_html, slate_tag_matches) 

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
