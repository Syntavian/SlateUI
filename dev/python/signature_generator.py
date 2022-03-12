import os

# The required Slate project structure to successfully build.
SIGNATURE: dict[str, list[str]] = {
    r".": ['build', 'dev'],
    r".\build": ['app'],
    r".\build\app": ['public', 'slate', 'src'],
    r".\build\app\src": ['public', 'app.js'],
    r".\build\app\src\public": ['css', 'html', 'js'],
    r".\build\app\src\public\html": ['components', 'pages'],
    r".\dev": ['css', 'js', 'python', 'scss', 'slate_dev.py'],
    r".\dev\js": ['button_styles.js', 'image_styles.js', 'layout_styles.js', 'main.js', 'scroll_styles.js', 'sticky_styles.js', 'theme_styles.js', 'utils.js'],
    r".\dev\python": ['css_build', 'html_build', 'js_build', 'utils', 'build.py', 'build_event_handler.py', 'debug.py', 'directories.py', 'signature_generator.py', 'thread_handler.py'],
    r".\dev\python\css_build": ['css_builder.py', 'find_required_styles.py'],
    r".\dev\python\html_build": ['argument_type.py', 'component.py', 'html_builder.py', 'html_templating.py', 'page.py', 'wrapper.py'],
    r".\dev\python\js_build": ['js_builder.py'],
    r".\dev\python\utils": ['console_utils.py', 'error_utils.py', 'file_utils.py', 'function_utils.py', 'html_utils.py', 'string_utils.py'],
    r".\dev\scss": ['elements', 'style.scss', '_borders.scss', '_fixed.scss', '_layout.scss', '_offsets.scss', '_prototypes.scss', '_shadow.scss', '_text.scss', '_variables.scss', '_z-index.scss'],
    r".\dev\scss\elements": ['_backgrounds.scss', '_box.scss', '_buttons.scss', '_canvas.scss', '_fade.scss', '_floating.scss', '_forms.scss', '_images.scss', '_links.scss', '_popup.scss'],
}

SIGNATURE_IGNORE = [
    r"node_modules",
    r"lib",
    r".github",
    r".gitignore",
    r".git",
    r".json",
    r".png",
    r".map",
    r".md",
    r".txt",
    r".log",
    r"__pycache__",
    r"\app\slate",
    r"\app\public",
    r"\app\src\public\css",
    r"\app\src\public\js",
    r"\app\src\public\html\pages",
    r"\app\src\public\html\components",
    r"\dev\css",
]


def generate(_path: str = ".") -> dict[str, list[str]]:
    signature = {}
    for dirpath, dirnames, filenames in os.walk(_path):
        if any([x in dirpath for x in SIGNATURE_IGNORE]):
            continue
        dir_contents = [x for x in dirnames if x not in SIGNATURE_IGNORE]
        dir_contents.extend([x for x in filenames if x not in SIGNATURE_IGNORE and not any(
            [y in x for y in SIGNATURE_IGNORE])])
        signature[dirpath] = dir_contents
    return signature


if __name__ == "__main__":
    result = generate()
    for k, v in result.items():
        print(f"    r\"{k}\": {v},")
