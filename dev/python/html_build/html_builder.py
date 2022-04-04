import os
import re
from typing import Iterator, Literal, Match

from python.debug import debug
from python.html_build.html_templating import *
from python.html_build.types.argument import ArgumentType
from python.html_build.types.component import Component
from python.html_build.types.page import Page
from python.html_build.types.tag import Tag
from python.html_build.types.wrapper import Wrapper, WrapperType
from python.utils.error_utils import *
from python.utils.file_utils import *
from python.utils.html_utils import *


@debug
def fast_check_wrapper(_html: str) -> bool:
    '''Return True if _html possibly contains a wrapper identifier'''
    if re.search(containing(r"\*"), _html):
        return True
    return False


@debug
def fast_check_global_assignment(_argument: str) -> bool:
    '''Return True if _argument is an assignment'''
    if re.search(containing(r"%.*="), _argument):
        return True
    return False


@debug
def get_wrapper(_slate_tag_content: str) -> Match[str]:
    '''Return a wrapper match if one is found, exception if multiple are found'''
    wrapper_matches = [wrapper_match for wrapper_match in re.finditer(containing(
        r"\*(?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$)\S*"), strip_slate_tag(_slate_tag_content))]
    if not wrapper_matches:
        return
    elif len(wrapper_matches) > 1:
        exception("Multiple wrappers found.")
        return
    return wrapper_matches[0]


@debug
def get_wrapper_type(_wrapper: str) -> Literal[WrapperType.COMPONENT, WrapperType.PAGE, WrapperType.ALL, WrapperType.INVALID]:
    '''Return the type of a wrapper'''
    if re.search(r"\*@\w+", _wrapper):
        return WrapperType.COMPONENT
    if re.search(r"\*\w+", _wrapper):
        return WrapperType.PAGE
    if re.search(r"\* |\*$", _wrapper):
        return WrapperType.ALL
    exception(f"wrapper {_wrapper} is not valid.")
    return WrapperType.INVALID


@debug
def build_wrapper(_html: str, _slate_tag_match: Match[str], _slate_tag_matches: list[Match[str]], _is_root: bool = False) -> Wrapper | None:
    '''Create a Wrapper instance'''
    # Find and validate the wrapper.
    wrapper = get_wrapper(_slate_tag_match.group(1))
    if not wrapper:
        return None
    wrapper_type = get_wrapper_type(wrapper.group(1))
    if _is_root and wrapper_type != WrapperType.ALL:
        exit_exception("Root HTML wrapper is not valid.")
    if wrapper_type == WrapperType.INVALID:
        exception("Wrapper is not valid.")
        return
    return Wrapper(wrapper_type, _html[:_slate_tag_match.start()], _html[_slate_tag_match.end():], wrapper.group(1), _slate_tag_matches)


@debug
def handle_wrapper_build(_html: str, _slate_tag_matches: Iterator[Match[str]], _wrappers: dict[str, list[Wrapper]], _is_root: bool = False) -> bool:
    '''Add a wrapper to _wrappers if one is found in _slate_tag_matches'''
    wrapper: Wrapper | None = None
    for slate_tag_match in _slate_tag_matches:
        if fast_check_wrapper(slate_tag_match.group(1)):
            newWrapper = build_wrapper(
                _html, slate_tag_match, _slate_tag_matches, _is_root)
            if newWrapper:
                if not wrapper:
                    wrapper = newWrapper
                else:
                    exit_exception("Multi-wrapper HTML is not valid.")
    if wrapper:
        if wrapper.wrapped_object not in _wrappers.keys():
            _wrappers[wrapper.wrapped_object] = []
        _wrappers[wrapper.wrapped_object].append(wrapper)
        return True
    return False


@debug
def reset_variables(_variables: dict[str, str], _global_variables: dict[str, str]) -> None:
    '''Empty _variables dict before adding the content of _global_variables to it'''
    _variables = {}
    for k, v in _global_variables.items():
        _variables[k] = v


@debug
def determine_argument_type(_argument: str) -> Literal[ArgumentType.VARIABLE_ASSIGNMENT, ArgumentType.GLOBAL_ASSIGNMENT, ArgumentType.INVALID, ArgumentType.ROOT_WRAPPER, ArgumentType.COMPONENT_WRAPPER, ArgumentType.PAGE_WRAPPER, ArgumentType.VARIABLE, ArgumentType.GLOBAL, ArgumentType.COMPONENT, ArgumentType.PAGE]:
    '''Return the Argument type of _argument based on the identifier and whether it is an assignment'''
    if '=' in _argument:
        if _argument[0] == '$':
            return ArgumentType.VARIABLE_ASSIGNMENT
        elif _argument[0] == '%':
            return ArgumentType.GLOBAL_ASSIGNMENT
        else:
            return ArgumentType.INVALID
    elif _argument[0] == '*':
        if len(_argument) == 1:
            return ArgumentType.ROOT_WRAPPER
        elif _argument[1] == '@':
            return ArgumentType.COMPONENT_WRAPPER
        else:
            return ArgumentType.PAGE_WRAPPER
    elif _argument[0] == '$':
        return ArgumentType.VARIABLE
    elif _argument[0] == '%':
        return ArgumentType.GLOBAL
    elif _argument[0] == '@':
        return ArgumentType.COMPONENT
    else:
        return ArgumentType.PAGE


@debug
def split_variable_assignment(_variable_assignment: str) -> tuple[str, str]:
    '''Split a variable assignment argument into the key and value components'''
    variable_assignment_split = re.split(
        r"=(?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$)", _variable_assignment)
    return (variable_assignment_split[0].strip(), variable_assignment_split[1].strip())


@debug
def split_slate_arguments(_slate_tag_match: Match[str]):
    '''Split a slate tag match into its component arguments'''
    arguments_string = strip_slate_tag(_slate_tag_match.group(1))
    split_arguments_string = re.split(
        r"((?<!=)[\s@$%*](?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$).*?)(?=(?<!=)[\s@$%*](?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$)|$)", arguments_string)
    arguments = []
    for argument in split_arguments_string:
        if len(argument) > 0 and not re.match(r"\s", argument):
            arguments.append(argument)
    return arguments


@debug
def apply_global_variables(_global_variables: dict[str, str], _slate_tag_matches: list[Match[str]]) -> None:
    '''Add all global variables from _slate_tag_matches into the _global_variables dict'''
    for match in _slate_tag_matches:
        arguments = split_slate_arguments(match)
        for argument in arguments:
            if fast_check_global_assignment(argument):
                if determine_argument_type(argument) == ArgumentType.GLOBAL_ASSIGNMENT:
                    variable, value = split_variable_assignment(argument)
                    _global_variables[variable] = value


@debug
def compute_slate_tags(_html: str, _global_variables: dict[str, str]) -> list[Tag]:
    '''Find and return all slate tags in _html, adding global variables to _global_variables'''
    slate_tag_matches = get_slate_tags(_html)
    apply_global_variables(_global_variables, slate_tag_matches)
    slate_tags = []
    for slate_tag_match in slate_tag_matches:
        slate_tags.append(Tag(
            slate_tag_match.start(),
            slate_tag_match.end() - slate_tag_match.start(),
            [slate_tag_match.group(1)]
        ))
    for slate_tag in slate_tags:
        print(slate_tag)
    return slate_tags


@debug
def build_html(_slate_dir: str, _html_in_dir: str, _html_out_dir: str) -> None:
    '''Build HTML files from Slate UI HTML templates for deployment'''
    # Global variables store
    global_variables: dict[str, str] = {}
    # Local variables store
    variables: dict[str, str] = {}
    # Component definitions
    components: dict[str, Component] = {}
    # Wrapper definitions
    wrappers: dict[str, list[Wrapper]] = {}
    # Page definitions
    pages: dict[str, Page] = {}

    # Get the root HTML wrapper from slate.html.
    with open(f"{_slate_dir}/slate.html", "r") as root_html_file:
        root_html = root_html_file.read()
        slate_tags = compute_slate_tags(root_html, global_variables)
        if not handle_wrapper_build(root_html, slate_tags, wrappers, True):
            exit_exception("Root HTML wrapper is not valid.")

    for dirpath, dirnames, filenames in os.walk(f"{_html_in_dir}/components"):
        for component_file_name in filenames:
            with open(dirpath + "\\" + component_file_name, "r") as component_html_file:
                component_file_name_text = get_file_name(component_file_name)
                component_html = component_html_file.read()
                slate_tags = compute_slate_tags(
                    component_html, global_variables)
                if not handle_wrapper_build(component_html, slate_tags, wrappers):
                    components[f"@{component_file_name_text}"] = Component(
                        component_html, slate_tags)

    for dirpath, dirnames, filenames in os.walk(f"{_html_in_dir}/pages"):
        for page_file_name in filenames:
            file_path = f"{dirpath}/{page_file_name}".replace('\\', '/')
            with open(file_path, "r") as page_html_file:
                page_html = page_html_file.read()
                slate_tags = compute_slate_tags(page_html, global_variables)
                pages[file_path] = Page(file_path.split(
                    f"{_html_in_dir}/pages")[1], page_html, slate_tags)

    for page_path, page in pages.items():
        reset_variables(variables, global_variables)

        html_page_result = process_html_page(
            page, variables, components, wrappers)

        OUTPUT_HTML_PATH = f"{_html_out_dir}{page.path}"
        os.makedirs(os.path.dirname(OUTPUT_HTML_PATH), exist_ok=True)
        with open(OUTPUT_HTML_PATH, "w") as html_output_file:
            html_output_file.write(html_page_result)
