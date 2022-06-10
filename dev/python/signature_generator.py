import os

# The required Slate project structure to successfully build
SIGNATURE: dict[str, list[str]] = {
    r".": [
        "build",
        "dev",
        ".prettierignore",
        ".prettierrc",
        ".swcrc",
        "jest.config.js",
        "spack.config.js",
    ],
    r".\build": ["app"],
    r".\build\app": ["public", "slate", "src", "jest.config.js"],
    r".\build\app\src": ["public", "app.js"],
    r".\build\app\src\public": ["css", "html", "js"],
    r".\build\app\src\public\html": ["components", "pages"],
    r".\dev": ["css", "js", "python", "scss", "ts", "slate_dev.py"],
    r".\dev\js": [],
    r".\dev\python": [
        "css_build",
        "html_build",
        "js_build",
        "utils",
        "build.py",
        "build_event_handler.py",
        "debug.py",
        "directories.py",
        "signature_generator.py",
        "thread_handler.py",
    ],
    r".\dev\python\css_build": ["css_builder.py", "find_required_styles.py"],
    r".\dev\python\html_build": ["types", "html_builder.py", "html_templating.py"],
    r".\dev\python\html_build\types": [
        "argument.py",
        "component.py",
        "page.py",
        "tag.py",
        "wrapper.py",
    ],
    r".\dev\python\js_build": ["js_builder.py"],
    r".\dev\python\utils": [
        "console_utils.py",
        "error_utils.py",
        "file_utils.py",
        "function_utils.py",
        "html_utils.py",
        "string_utils.py",
        "test_file_utils.py",
        "test_function_utils.py",
        "test_html_utils.py",
        "test_string_utils.py",
    ],
    r".\dev\scss": [
        "elements",
        "style.scss",
        "_borders.scss",
        "_fixed.scss",
        "_layout.scss",
        "_offsets.scss",
        "_prototypes.scss",
        "_shadow.scss",
        "_text.scss",
        "_variables.scss",
        "_z-index.scss",
    ],
    r".\dev\scss\elements": [
        "_backgrounds.scss",
        "_box.scss",
        "_buttons.scss",
        "_canvas.scss",
        "_fade.scss",
        "_floating.scss",
        "_forms.scss",
        "_images.scss",
        "_links.scss",
        "_popup.scss",
    ],
    r".\dev\ts": [
        "buttonStyles.ts",
        "cssUtils.test.ts",
        "cssUtils.ts",
        "imageStyles.ts",
        "layoutStyles.ts",
        "main.ts",
        "scrollStyles.ts",
        "stickyStyles.ts",
        "themeStyles.ts",
        "typeUtils.test.ts",
        "typeUtils.ts",
    ],
}

SIGNATURE_IGNORE = [
    r"node_modules",
    r"__pycache__",
    r"coverage",
    r"pytest",
    r"lib",
    r".pytest_cache",
    r".gitignore",
    r".github",
    r".git",
    r".json",
    r".png",
    r".map",
    r".txt",
    r".log",
    r".md",
    r"\dev\css",
    r"\app\slate",
    r"\app\public",
    r"\app\src\public\css",
    r"\app\src\public\js",
    r"\app\src\public\html\pages",
    r"\app\src\public\html\components",
]


def generate(_path: str = ".") -> dict[str, list[str]]:
    signature = {}
    for dirpath, dirnames, filenames in os.walk(_path):
        if any([x in dirpath for x in SIGNATURE_IGNORE]):
            continue
        dir_contents = [x for x in dirnames if x not in SIGNATURE_IGNORE]
        dir_contents.extend(
            [
                x
                for x in filenames
                if x not in SIGNATURE_IGNORE
                and not any([y in x for y in SIGNATURE_IGNORE])
            ]
        )
        signature[dirpath] = dir_contents
    return signature


if __name__ == "__main__":
    result = generate()
    for k, v in result.items():
        print(f'    r"{k}": {v},')
