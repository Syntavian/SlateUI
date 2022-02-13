import os

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
        print(f"r\"{k}\": {v},")
