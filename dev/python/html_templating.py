class HTMLSubstitution:
    def __init__(self, args: list[str], before: str, after: str, continues: bool) -> None:
        self.args = args
        self.before = before
        self.after = after
        self.continues = continues

def merge_string_arguments(args: list[str]) -> list[str]:
    corrected_line_values: list[str] = []
    is_string = False

    for value in args:
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

def identify_substitutions(text: str) -> HTMLSubstitution:
    args: list[str] = []
    before = ""
    after = ""

    # TODO: Remove the reliance on HTML comment tags by specifying new syntax.

    if r"<!--" in text and r"-->" in text:
        comment_start = text.find(r"<!--")
        comment_end = text.find(r"-->")
        before = text[0:comment_start]
        after = text[comment_end + 3:]
        args = text[comment_start + 4:comment_end].strip().split()
    args = merge_string_arguments(args)

    continues = (r"<!--" in after and r"-->" in after)

    return HTMLSubstitution(args, before, after, continues)

def extract_variables(arguments: list[str], templates: list[str], variables: list[str]) -> list[str]:
    result_variables = variables

    for argument in arguments:
        if '=' in argument:
            variable = argument.split("=")
            if variable[1][0] == "":
                pass
            elif variable[1][0] == '"':
                result_variables[variable[0]] = variable[1].replace('"', "")
            elif variable[1][0] == '$':
                try:
                    result_variables[variable[0]] = variables[variable[0]]
                except:
                    result_variables[variable[0]] = ""
            else:
                result_variables[variable[0]] = process_template(variable[1], templates, variables)

    return result_variables

def perform_substitution(text: str, substitution: HTMLSubstitution, templates: list[str], variables: list[str]) -> tuple[str, list[str]]:
    result_text = text + substitution.before
    variables = extract_variables(substitution.args, templates, variables)

    if substitution.args[0][0] == '$':
        result_text = result_text + variables[substitution.args[0]]
    else:
        result_text = result_text + process_template(substitution.args[0], templates, variables)
    if not substitution.continues:
        result_text = result_text + substitution.after

    return result_text, variables

def process_template(template_name: str, variables: list[str], templates: list[str]) -> str:
    template = templates[template_name]

    return process_text(template, variables, templates)

def process_text(text: str, variables: list[str], templates: list[str]) -> str:
    result_text = ""
    substitution = identify_substitutions(text)

    if len(substitution.args) > 0: 
        result_text, variables = perform_substitution(result_text, substitution, templates, variables)
        if substitution.continues:
            while substitution.continues:
                substitution = identify_substitutions(substitution.after)
                if len(substitution.args) > 0: 
                    result_text, variables = perform_substitution(result_text, substitution, templates, variables)
    else:
        result_text = text

    return result_text
