import subprocess
import time
import os
from watchdog.observers import Observer
from python.directories import *
from python.string_utils import *
from python.build import build
from python.thread_handler import ThreadHandler
from python.build_event_handler import ModifiedEventBuildEventHandler

# The required Slate project structure to successfully build.
SIGNATURE: dict[str, list[str]] = {
    r".": ["build", "dev"],
    r".\build": ["app"],
    r".\build\app": ["lib", "public", "slate", "src"],
    r".\build\app\public": ["css", "img", "js"],
    r".\build\app\src": ["public"],
    r".\build\app\src\public": ["css", "html", "js"],
    r".\build\app\src\public\html": ["components", "pages"],
    r".\dev": ["css", "js", "python", "scss"],
    r".\dev\js": ["lib", "src"],
    r".\dev\python": [],
    r".\dev\scss": ["elements"],
}

if __name__ == "__main__":
    # Verify the project structure.
    for (dirpath, dirnames, filenames) in os.walk("."):
        if (dirpath in SIGNATURE.keys() and not all([x in dirnames for x in SIGNATURE[dirpath]])):
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
