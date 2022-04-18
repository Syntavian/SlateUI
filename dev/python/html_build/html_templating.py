from python.debug import debug
from python.html_build.types.component import Component
from python.html_build.types.page import Page
from python.html_build.types.tag import Tag
from python.html_build.types.wrapper import Wrapper


@debug
def merge_string_arguments(_args: list[str]) -> list[str]:
    corrected_line_values: list[str] = []
    is_string = False

    for value in _args:
        if value.count('"') == 1 or value.count("'") == 1:
            if not is_string:
                corrected_line_values.append(value)
                is_string = True
            else:
                corrected_line_values[-1] = corrected_line_values[-1] + " " + value
                is_string = False
        else:
            if is_string:
                corrected_line_values[-1] = corrected_line_values[-1] + " " + value
            else:
                corrected_line_values.append(value)

    return corrected_line_values


@debug
def extract_variables(
    _arguments: list[str], _templates: list[str], _variables: list[str]
) -> list[str]:
    result_variables = _variables

    for argument in _arguments:
        if "=" in argument:
            variable = argument.split("=")
            if variable[1][0] == "":
                pass
            elif variable[1][0] == '"':
                result_variables[variable[0]] = variable[1].replace('"', "")
            elif variable[1][0] == "$":
                try:
                    result_variables[variable[0]] = _variables[variable[0]]
                except:
                    result_variables[variable[0]] = ""
            else:
                result_variables[variable[0]] = process_template(
                    variable[1], _templates, _variables
                )

    return result_variables


@debug
def perform_substitution(
    _html: str,
    _tag: Tag,
    _variables: list[str],
    _components: dict[str, Component],
    _wrappers: dict[str, list[Wrapper]],
) -> tuple[str, list[str]]:
    result_html = _html[0 : _tag.position]
    _variables = extract_variables(_tag.arguments, _variables)

    return result_html


@debug
def process_template(
    _template_name: str, _variables: list[str], _templates: list[str]
) -> str:
    template = _templates[_template_name]
    return process_html_page(template, _variables, _templates)


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
