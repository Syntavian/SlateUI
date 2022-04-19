import re

from python.debug import debug
from python.html_build.types.argument import Argument, ArgumentType
from python.html_build.types.component import Component
from python.html_build.types.page import Page
from python.html_build.types.tag import Tag
from python.html_build.types.wrapper import Wrapper


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
def perform_substitution(
    _html: str,
    _tag: Tag,
    _variables: dict[str, str],
    _components: dict[str, Component],
    _wrappers: dict[str, list[Wrapper]],
) -> tuple[str, list[str]]:
    # Local copy of _variables for this substitution
    variables = _variables.copy()
    result_html = _html[0 : _tag.position]

    print(variables)
    print(_tag)

    for argument in _tag.arguments:
        if argument.type == ArgumentType.VARIABLE_ASSIGNMENT:
            apply_variable(variables, argument)

    if _tag.arguments[0].type == ArgumentType.COMPONENT:
        result_html += _components[_tag.arguments[0].value].html
    print(result_html)
    exit()
    return result_html


@debug
def process_html_page(
    _page: Page,
    _variables: dict[str, str],
    _components: dict[str, Component],
    _wrappers: dict[str, list[Wrapper]],
) -> str:
    """Build a HTML page from templates"""
    result_html = ""
    # substitution = identify_substitutions(_page.tags)

    if len(_page._tags) > 0:
        for tag in _page._tags:
            result_html = perform_substitution(
                _page._html, tag, _variables, _components, _wrappers
            )
    else:
        result_html = _page._html

    return result_html
