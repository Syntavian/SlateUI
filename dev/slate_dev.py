import subprocess
import time
import os
from watchdog.observers import Observer
from python.directories import *
from python.string_utils import *
from python.build import build
from python.thread_handler import ThreadHandler
from python.build_event_handler import ModifiedEventBuildEventHandler
from python.signature_generator import SIGNATURE_IGNORE

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
    r".\dev\python": ['build.py', 'build_event_handler.py', 'css_builder.py', 'directories.py', 'find_required_styles.py', 'html_builder.py', 'html_templating.py', 'js_builder.py', 'signature_generator.py', 'string_utils.py', 'thread_handler.py', 'transfer_file.py'],
    r".\dev\scss": ['elements', 'style.scss', '_borders.scss', '_fixed.scss', '_layout.scss', '_offsets.scss', '_prototypes.scss', '_shadow.scss', '_text.scss', '_variables.scss', '_z-index.scss'],
    r".\dev\scss\elements": ['_backgrounds.scss', '_box.scss', '_buttons.scss', '_canvas.scss', '_fade.scss', '_floating.scss', '_forms.scss', '_images.scss', '_links.scss', '_popup.scss'],
}

if __name__ == "__main__":
    # Verify the project structure.
    for (dirpath, dirnames, filenames) in os.walk("."):
        if any([x in dirpath for x in SIGNATURE_IGNORE]):
            continue
        dir_contents = dirnames
        dir_contents.extend(filenames)
        if (dirpath in SIGNATURE.keys() and not all([x in dir_contents for x in SIGNATURE[dirpath]])):
            print(f"Error: Project signature mismatch at: '{dirpath}' requires: '{SIGNATURE[dirpath]}'.")
            exit()
    # Start SASS watch to compile SCSS into CSS every time there is a change.
    subprocess.Popen(["sass", "--watch", f"{SCSS_PREBUILD_DIR}:{CSS_PREBUILD_DIR}"])
    # Wait for SASS to complete then build Slate once on run.
    time.sleep(1)
    build()
    # Create the event handler to store and handle file modification events in the project.
    event_handler = ModifiedEventBuildEventHandler()
    # Create an observer for file update events.
    observer = Observer()
    # Schedule the event handler to run on events in dev css directory.
    observer.schedule(event_handler, CSS_PREBUILD_DIR)
    observer.start()
    # Create the thread handler for build threads. 
    thread_handler = ThreadHandler(build)
    try:
        while True:
            time.sleep(1)
            # Call the event handler to run the thread handler every tick if a file event has occurred.
            event_handler.update(thread_handler)
    finally:
        observer.stop()
        thread_handler.stop()
        observer.join()
        exit()
