import os
import re
from typing import Match

from python.debug import *
from python.html_build.html_templating import *
from python.html_build.types.argument import *
from python.html_build.types.component import *
from python.html_build.types.page import *
from python.html_build.types.tag import *
from python.html_build.types.wrapper import *
from python.utils.error_utils import *
from python.utils.file_utils import *
from python.utils.html_utils import *


@debug
def get_wrapper(_slate_tag_content: str) -> Match[str]:
    """Return a wrapper match if one is found, exception if multiple are found"""
    wrapper_matches = [
        wrapper_match
        for wrapper_match in re.finditer(
            containing(r"\*(?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$)\S*"),
            strip_slate_tag(_slate_tag_content),
        )
    ]
    if not wrapper_matches:
        return
    elif len(wrapper_matches) > 1:
        exception("Multiple wrappers found.")
        return
    return wrapper_matches[0]


@debug
def build_wrapper(
    _html: str, _slate_tag: Tag, _slate_tag_matches: list[Tag], _is_root: bool = False
) -> Wrapper | None:
    """Create a Wrapper instance"""
    # Find and validate the wrapper.
    wrapper = get_wrapper(_slate_tag.text)
    if not wrapper:
        return None
    wrapper_type = determine_wrapper_type(wrapper.group(1))
    if _is_root and wrapper_type != WrapperType.ALL:
        exit_exception("Root HTML wrapper is not valid.")
    if wrapper_type == WrapperType.INVALID:
        exception("Wrapper is not valid.")
        return
    return Wrapper(
        wrapper_type,
        _html[: _slate_tag.position],
        _html[_slate_tag.position + _slate_tag.length :],
        wrapper.group(1),
        _slate_tag_matches,
    )


@debug
def handle_wrapper_build(
    _html: str,
    _slate_tags: list[Tag],
    _wrappers: dict[str, list[Wrapper]],
    _is_root: bool = False,
) -> bool:
    """Add a wrapper to _wrappers if one is found in _slate_tag_matches"""
    wrapper: Wrapper | None = None
    for slate_tag in _slate_tags:
        newWrapper = build_wrapper(_html, slate_tag, _slate_tags, _is_root)
        if newWrapper:
            if not wrapper:
                wrapper = newWrapper
            else:
                exit_exception("Multi-wrapper HTML is not valid.")
    if wrapper:
        if wrapper._wrapped_object not in _wrappers.keys():
            _wrappers[wrapper._wrapped_object] = []
        _wrappers[wrapper._wrapped_object].append(wrapper)
        return True
    return False


@debug
def reset_variables(
    _variables: dict[str, str], _global_variables: dict[str, str]
) -> None:
    """Empty _variables dict before adding the content of _global_variables to it"""
    _variables.clear()
    for k, v in _global_variables.items():
        _variables[k] = v
    print(_variables)


@debug
def split_slate_arguments(_slate_tag_match: Match[str]) -> list[str]:
    """Split a slate tag match into its component arguments"""
    arguments_string = strip_slate_tag(_slate_tag_match.group(1))
    split_arguments_string = re.split(
        r"((?<!=)[\s@$%*](?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$).*?)(?=(?<!=)[\s@$%*](?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$)|$)",
        arguments_string,
    )
    arguments = []
    for argument in split_arguments_string:
        if len(argument) > 0 and not re.match(r"\s", argument):
            arguments.append(argument)
    return arguments


@debug
def process_arguments(
    _arguments: list[str], _global_variables: dict[str, str]
) -> tuple[list[Argument], bool]:
    """Returns a list of Argument instances and sets all global variable arguments for each argument in the string _arguments, along with a boolean True if one of the arguments denotes is a wrapper type"""
    processed_arguments = []
    has_wrapper_argument = False
    for argument in _arguments:
        argument_type = determine_argument_type(argument)
        if argument_type == ArgumentType.GLOBAL_ASSIGNMENT:
            apply_variable(_global_variables, argument)
            continue
        elif argument_type in [
            ArgumentType.ROOT_WRAPPER,
            ArgumentType.PAGE_WRAPPER,
            ArgumentType.COMPONENT_WRAPPER,
        ]:
            has_wrapper_argument = True
        processed_arguments.append(Argument(argument, argument_type))
    return (processed_arguments, has_wrapper_argument)


@debug
def compute_slate_tags(
    _html: str, _global_variables: dict[str, str]
) -> tuple[list[Tag], bool]:
    """Find and return all slate tags in _html, adding global variables to _global_variables"""
    slate_tags = []
    is_wrapper_html = False
    slate_tag_matches = get_slate_tags(_html)
    for slate_tag_match in slate_tag_matches:
        arguments = split_slate_arguments(slate_tag_match)
        (processed_arguments, has_wrapper_argument) = process_arguments(
            arguments, _global_variables
        )
        if has_wrapper_argument:
            is_wrapper_html = True
        slate_tags.append(
            Tag(
                slate_tag_match.start(),
                slate_tag_match.end() - slate_tag_match.start(),
                slate_tag_match.group(1),
                processed_arguments,
            )
        )
    for slate_tag in slate_tags:
        print(slate_tag, "\n")
    return (slate_tags, is_wrapper_html)


@debug
def build_html(_slate_dir: str, _html_in_dir: str, _html_out_dir: str) -> None:
    """Build HTML files from Slate UI HTML templates for deployment"""
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
        (slate_tags, is_wrapper_html) = compute_slate_tags(root_html, global_variables)
        if not is_wrapper_html or not handle_wrapper_build(
            root_html, slate_tags, wrappers, True
        ):
            exit_exception("Root HTML wrapper is not valid.")

    for dirpath, dirnames, filenames in os.walk(f"{_html_in_dir}/components"):
        for component_file_name in filenames:
            with open(dirpath + "\\" + component_file_name, "r") as component_html_file:
                component_file_name_text = get_file_name(component_file_name)
                component_html = component_html_file.read()
                (slate_tags, is_wrapper_html) = compute_slate_tags(
                    component_html, global_variables
                )
                if not is_wrapper_html or not handle_wrapper_build(
                    component_html, slate_tags, wrappers
                ):
                    components[f"@{component_file_name_text}"] = Component(
                        component_html, slate_tags
                    )

    for dirpath, dirnames, filenames in os.walk(f"{_html_in_dir}/pages"):
        for page_file_name in filenames:
            file_path = f"{dirpath}/{page_file_name}".replace("\\", "/")
            with open(file_path, "r") as page_html_file:
                page_html = page_html_file.read()
                (slate_tags, _) = compute_slate_tags(page_html, global_variables)
                pages[file_path] = Page(
                    file_path.split(f"{_html_in_dir}/pages")[1], page_html, slate_tags
                )

    for key in components:
        print(components[key], "\n")

    for key in wrappers:
        for wrapper in wrappers[key]:
            print(wrapper, "\n")

    for key in pages:
        print(pages[key], "\n")

    for key in global_variables:
        print(f"{key}: {global_variables[key]}\n")

    for page_path, page in pages.items():
        reset_variables(variables, global_variables)

        html_page_result = process_html_page(page, variables, components, wrappers)

        OUTPUT_HTML_PATH = f"{_html_out_dir}{page._path}"
        os.makedirs(os.path.dirname(OUTPUT_HTML_PATH), exist_ok=True)
        with open(OUTPUT_HTML_PATH, "w") as html_output_file:
            html_output_file.write(html_page_result)
