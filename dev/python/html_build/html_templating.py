import re

from python.debug import debug
from python.html_build.types.argument import Argument, ArgumentType
from python.html_build.types.component import Component
from python.html_build.types.page import Page
from python.html_build.types.tag import Tag
from python.html_build.types.wrapper import ComputedWrapper, Wrapper


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

    print(variables)
    print(_tag)

    for argument in reversed(_tag.arguments):
        match argument.type:
            case ArgumentType.VARIABLE_ASSIGNMENT:
                apply_variable(variables, argument)
                print(variables)
            case ArgumentType.COMPONENT:
                result_html += process_component(
                    _components[argument.value], variables, _components, _wrappers
                )
            case ArgumentType.GLOBAL:
                result_html += _variables[argument.value]
            case ArgumentType.VARIABLE:
                result_html += _variables[argument.value]

    return result_html


@debug
def process_wrapper(
    _wrapper: Wrapper,
    _variables: dict[str, str],
    _components: dict[str, Component],
) -> ComputedWrapper:
    """Process a wrapper and return the processed HTML content"""

    return ComputedWrapper(_wrapper.before, _wrapper.after)


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
    wrappers = []

    # Add the root HTML Wrapper to the component Wrappers list
    if _is_page:
        wrappers.append(process_wrapper(_wrappers["*"][0], _variables, _components))

    if _component.id in _wrappers.keys():
        wrappers.extend(
            [
                process_wrapper(wrapper, _variables, _components)
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
