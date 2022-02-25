import os
import re
from typing import Iterator, Literal, Match
from python.html_build.page import Page
from python.html_build.component import Component
from python.html_build.wrapper import Wrapper, WrapperType
from python.utils.file_utils import *
from python.utils.html_utils import *
from python.utils.error_utils import *
from python.html_build.html_templating import *

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

def reset_variables(_variables: dict[str, str], _global_variables: dict[str, str]) -> None:
    _variables = {}
    for k, v in _global_variables.items():
        _variables[k] = v

# TODO: Create arg type Enum.
def determine_argument_type(_argument: str) -> str:
    if '=' in _argument:
        if _argument[0] == '$':
            return 'variable'
        elif _argument[0] == '%':
            return 'global'
        else:
            return None

def split_variable_assignment(_variable_assignment: str) -> tuple[str, str]:
    variable_assignment_split = re.split(r"=(?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$)", _variable_assignment)
    return (variable_assignment_split[0].strip(), variable_assignment_split[1].strip())

def apply_global_variables(_global_variables: dict[str, str], _slate_tag_matches: list[Match[str]]) -> None:
    for match in _slate_tag_matches:
        # TODO: split arguments with a better method than new line.
        arguments = re.split(r"\s(?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$)", strip_slate_tag(match.group(1)))
        for argument in arguments:
            if determine_argument_type(argument) == 'global':
                variable, value = split_variable_assignment(argument)
                _global_variables[variable] = value


def build_html(_slate_dir, _html_in_dir, _html_out_dir) -> None:
    # Global variables store
    global_variables: dict[str, str] = {}
    # Local variables store
    variables: dict[str, str]  = {}
    # Component definitions
    components: dict[str, Component] = {}
    # Wrapper definitions
    wrappers: dict[str, list[Wrapper]] = {}
    # Page definitions
    pages: dict[str, Page] = {}

    # Get the root HTML wrapper from slate.html.
    with open(f"{_slate_dir}/slate.html", "r") as root_html_file:
        root_html = root_html_file.read() 
        slate_tag_matches = get_slate_tags(root_html)
        apply_global_variables(global_variables, slate_tag_matches)
        if not handle_wrapper_build(root_html, slate_tag_matches, wrappers, True):
            exit_exception("Root HTML wrapper is not valid.")

    for dirpath, dirnames, filenames in os.walk(f"{_html_in_dir}/components"):
        for component_file_name in filenames:
            with open(dirpath + "\\" + component_file_name, "r") as component_html_file:
                component_file_name_text = get_file_name(component_file_name)
                component_html = component_html_file.read()
                slate_tag_matches = get_slate_tags(component_html)
                apply_global_variables(global_variables, slate_tag_matches)
                if not handle_wrapper_build(component_html, slate_tag_matches, wrappers):
                    components[f"@{component_file_name_text}"] = Component(component_html, slate_tag_matches) 

    for dirpath, dirnames, filenames in os.walk(f"{_html_in_dir}/pages"):
        for page_file_name in filenames:
            file_path = f"{dirpath}/{page_file_name}".replace('\\', '/')
            with open(file_path, "r") as page_html_file:
                page_html = page_html_file.read()
                slate_tag_matches = get_slate_tags(page_html)
                apply_global_variables(global_variables, slate_tag_matches)
                pages[file_path] = Page(file_path.split(f"{_html_in_dir}/pages")[1], page_html, slate_tag_matches) 

    for page_path, page in pages.items():
        reset_variables(variables, global_variables)

        # current_page_result = process_html(page.html, variables, components, wrappers)

        OUTPUT_HTML_PATH = f"{_html_out_dir}{page.path}"
        os.makedirs(os.path.dirname(OUTPUT_HTML_PATH), exist_ok=True)
        with open(OUTPUT_HTML_PATH, "w") as html_output_file:
            html_output_file.write(page.html)
