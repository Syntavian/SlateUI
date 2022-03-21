from python.debug import debug
from python.html_build.component import Component
from python.html_build.page import Page
from python.html_build.wrapper import Wrapper


class HTMLSubstitution:
    def __init__(self, _args: list[str], _before: str, _after: str, _continues: bool) -> None:
        self.args = _args
        self.before = _before
        self.after = _after
        self.continues = _continues


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
                corrected_line_values[-1] = corrected_line_values[-1] + ' ' + value
                is_string = False
        else:
            if is_string:
                corrected_line_values[-1] = corrected_line_values[-1] + ' ' + value
            else:
                corrected_line_values.append(value)

    return corrected_line_values


@debug
def identify_substitutions(_text: str) -> HTMLSubstitution:
    args: list[str] = []
    before = ""
    after = ""

    # TODO: Remove the reliance on HTML comment tags by specifying new syntax.

    if r"<!--" in _text and r"-->" in _text:
        comment_start = _text.find(r"<!--")
        comment_end = _text.find(r"-->")
        before = _text[0:comment_start]
        after = _text[comment_end + 3:]
        args = _text[comment_start + 4:comment_end].strip().split()
    args = merge_string_arguments(args)

    continues = (r"<!--" in after and r"-->" in after)

    return HTMLSubstitution(args, before, after, continues)


@debug
def extract_variables(_arguments: list[str], _templates: list[str], _variables: list[str]) -> list[str]:
    result_variables = _variables

    for argument in _arguments:
        if '=' in argument:
            variable = argument.split("=")
            if variable[1][0] == "":
                pass
            elif variable[1][0] == '"':
                result_variables[variable[0]] = variable[1].replace('"', "")
            elif variable[1][0] == '$':
                try:
                    result_variables[variable[0]] = _variables[variable[0]]
                except:
                    result_variables[variable[0]] = ""
            else:
                result_variables[variable[0]] = process_template(
                    variable[1], _templates, _variables)

    return result_variables


@debug
def perform_substitution(_text: str, _substitution: HTMLSubstitution, _templates: list[str], _variables: list[str]) -> tuple[str, list[str]]:
    result_text = _text + _substitution.before
    _variables = extract_variables(_substitution.args, _templates, _variables)

    if _substitution.args[0][0] == '$':
        result_text: str = result_text + _variables[_substitution.args[0]]
    else:
        result_text: str = result_text + \
            process_template(_substitution.args[0], _templates, _variables)
    if not _substitution.continues:
        result_text: str = result_text + _substitution.after

    return result_text, _variables


def process_template(_template_name: str, _variables: list[str], _templates: list[str]) -> str:
    template = _templates[_template_name]

    return process_html_page(template, _variables, _templates)


@debug
def process_html_page(_page: Page, _variables: dict[str, str], _components: dict[str, Component], _wrappers: dict[str, list[Wrapper]]) -> str:
    result_html = ""
    substitution = identify_substitutions(_page.tag_matches)

    if len(substitution.args) > 0:
        result_html, _variables = perform_substitution(
            result_html, substitution, _components, _variables)
        if substitution.continues:
            while substitution.continues:
                substitution = identify_substitutions(substitution.after)
                if len(substitution.args) > 0:
                    result_html, _variables = perform_substitution(
                        result_html, substitution, _components, _variables)
    else:
        result_html = _page.html

    return result_html
