import os

# The required Slate project structure to successfully build.
SIGNATURE: dict[str, list[str]] = {
    r".": ['build', 'dev'],
    r".\build": ['app'],
    r".\build\app": ['lib', 'public', 'slate', 'src'],
    r".\build\app\lib": [],
    r".\build\app\public": ['css', 'img', 'js', 'index.html'],
    r".\build\app\public\css": ['slate.css'],
    r".\build\app\public\img": [],
    r".\build\app\public\js": ['slate.js'],
    r".\build\app\slate": ['slate.css', 'slate.html', 'slate.py'],
    r".\build\app\src": ['public', 'app.js'],
    r".\build\app\src\public": ['css', 'html', 'js'],
    r".\build\app\src\public\css": ['style.css'],
    r".\build\app\src\public\html": ['components', 'pages'],
    r".\build\app\src\public\html\pages": ['index.html'],
    r".\build\app\src\public\js": ['index.js'],
    r".\dev": ['css', 'js', 'python', 'scss', 'slate_dev.py'],
    r".\dev\css": ['style.css'],
    r".\dev\js": ['lib', 'src'],
    r".\dev\js\lib": [],
    r".\dev\js\src": ['button_styles.js', 'image_styles.js', 'layout_styles.js', 'scroll_styles.js', 'sticky_styles.js', 'theme_styles.js', 'utils.js'],
    r".\dev\python": ['build.py', 'build_event_handler.py', 'css_builder.py', 'directories.py', 'file_utils.py', 'find_required_styles.py', 'html_builder.py', 'html_templating.py', 'js_builder.py', 'signature_generator.py', 'string_utils.py', 'thread_handler.py', 'transfer_file.py'],
    r".\dev\scss": ['elements', 'style.scss', '_borders.scss', '_fixed.scss', '_layout.scss', '_offsets.scss', '_prototypes.scss', '_shadow.scss', '_text.scss', '_variables.scss', '_z-index.scss'],
    r".\dev\scss\elements": ['_backgrounds.scss', '_box.scss', '_buttons.scss', '_canvas.scss', '_fade.scss', '_floating.scss', '_forms.scss', '_images.scss', '_links.scss', '_popup.scss'],
}

SIGNATURE_IGNORE = [
    "node_modules",
    ".github",
    ".gitignore",
    ".git",
    ".json",
    ".png",
    ".map",
    ".md",
    "__pycache__",
    "app\src\public\html\components",
]

def generate(_path: str = ".") -> dict[str, list[str]]:
    signature = {}
    for dirpath, dirnames, filenames in os.walk(_path):
        if any([x in dirpath for x in SIGNATURE_IGNORE]):
            continue
        dir_contents = [x for x in dirnames if x not in SIGNATURE_IGNORE]
        dir_contents.extend([x for x in filenames if x not in SIGNATURE_IGNORE and not any([y in x for y in SIGNATURE_IGNORE])])
        signature[dirpath] = dir_contents
    return signature

if __name__ == "__main__":
    result = generate()
    for k, v in result.items():
        print(f"    r\"{k}\": {v},")
