import re

from python.debug import *
from python.html_build.types.argument import *
from python.html_build.types.component import *
from python.html_build.types.page import *
from python.html_build.types.tag import *
from python.html_build.types.wrapper import *
from python.utils.error_utils import *
from python.utils.file_utils import *
from python.utils.html_utils import *


@debug
def get_wrapper(_slate_tag_content: str) -> (Match[str] | None):
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
def split_variable_assignment(_variable_assignment: str) -> tuple[str, str]:
    """Split a variable assignment argument into the key and value components"""
    variable_assignment_split = re.split(
        r"=(?=(?:(?:[^\"]*\"[^\"]*\")|(?:[^']*'[^']*'))*[^\"']*$)", _variable_assignment
    )
    return (variable_assignment_split[0].strip(), variable_assignment_split[1].strip())


@debug
def apply_variable(_variables: dict[str, str], _argument: Argument | str) -> None:
    """Add global variable from _argument into the _global_variables dict"""
    variable, value = (
        split_variable_assignment(_argument.value)
        if isinstance(_argument, Argument)
        else split_variable_assignment(_argument)
    )
    _variables[variable] = value


@debug
def process_variable(
    _variable_value: str,
    _variables: dict[str, str],
    _components: dict[str, Component],
    _wrappers: dict[str, list[Wrapper]],
) -> str:
    """Process a variable"""
    if _variable_value in _variables.keys():
        return process_variable(_variables[_variable_value])
    elif _variable_value in _components.keys():
        return process_component(
            _components[_variable_value], _variables, _components, _wrappers
        )
    else:
        return _variable_value[1:-1]


@debug
def build_substitution(
    _tag: Tag,
    _variables: dict[str, str],
    _components: dict[str, Component],
    _wrappers: dict[str, list[Wrapper]],
) -> tuple[str, list[str]]:
    """Substitute a Slate Tag for processed HTML content based on the Tag's content and current state of _variables, _components, and _wrappers"""
    # Local copy of _variables for this substitution
    variables = _variables.copy()
    result_html = ""

    print(_tag)

    for argument in reversed(_tag.arguments):
        match argument.type:
            case ArgumentType.VARIABLE_ASSIGNMENT:
                apply_variable(variables, argument)
            case ArgumentType.COMPONENT:
                result_html += process_component(
                    _components[argument.value], variables, _components, _wrappers
                )
            case ArgumentType.GLOBAL:
                result_html += process_variable(
                    _variables[argument.value], _variables, _components, _wrappers
                )
            case ArgumentType.VARIABLE:
                result_html += process_variable(
                    _variables[argument.value], _variables, _components, _wrappers
                )

    return result_html


@debug
def process_wrapper(
    _wrapper: Wrapper,
    _variables: dict[str, str],
    _components: dict[str, Component],
    _wrappers: dict[str, list[Wrapper]],
) -> ComputedWrapper:
    """Process a wrapper and return the processed HTML content"""

    is_before_wrapper = True
    result_html_before_wrapper = ""
    result_html_after_wrapper = ""
    for index, tag in enumerate(_wrapper.tags):
        wrapper = get_wrapper(tag.text)
        last_tag = _wrapper.tags[index - 1]
        substitution_start = 0 if index == 0 else last_tag.position + last_tag.length
        if is_before_wrapper:
            result_html_before_wrapper += _wrapper.html[
                substitution_start : tag.position
            ] + build_substitution(tag, _variables, _components, _wrappers)
        else:
            result_html_after_wrapper += _wrapper.html[
                substitution_start : tag.position
            ] + build_substitution(tag, _variables, _components, _wrappers)
        if wrapper:
            is_before_wrapper = False

    substitution_start = (
        0 if index == 0 else _wrapper.tags[-1].position + _wrapper.tags[-1].length
    )

    result_html_after_wrapper += _wrapper.html[substitution_start:]

    return ComputedWrapper(
        result_html_before_wrapper,
        result_html_after_wrapper,
    )


@debug
def process_component(
    _component: Component,
    _variables: dict[str, str],
    _components: dict[str, Component],
    _wrappers: dict[str, list[Wrapper]],
    _is_page: bool = False,
) -> str:
    """Build a HTML component substitution from _variables, _components, and _wrappers"""
    result_html = ""
    wrappers: list[ComputedWrapper] = []

    # Add the root HTML Wrapper to the component Wrappers list
    if _is_page:
        wrappers.append(
            process_wrapper(_wrappers["*"][0], _variables, _components, _wrappers)
        )

    if _component.id in _wrappers.keys():
        wrappers.extend(
            [
                process_wrapper(wrapper, _variables, _components, _wrappers)
                for wrapper in _wrappers[_component.id]
            ]
        )

    for wrapper in wrappers:
        result_html += wrapper.before

    if len(_component.tags) > 0:
        for index, tag in enumerate(_component.tags):
            if index > 0:
                last_tag = _component.tags[index - 1]
                result_html += _component.html[
                    last_tag.position + last_tag.length : tag.position
                ]
            else:
                result_html += _component.html[0 : tag.position]
            result_html += build_substitution(tag, _variables, _components, _wrappers)
        last_tag = _component.tags[-1]
        result_html += _component.html[last_tag.position + last_tag.length :]
    else:
        result_html += _component.html

    for wrapper in reversed(wrappers):
        result_html += wrapper.after

    return result_html


@debug
def process_page(
    _page: Page,
    _variables: dict[str, str],
    _components: dict[str, Component],
    _wrappers: dict[str, list[Wrapper]],
) -> str:
    """Build a HTML page from templates"""

    return process_component(_page, _variables, _components, _wrappers, True)
