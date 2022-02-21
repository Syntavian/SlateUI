import subprocess
import time
import os
from watchdog.observers import Observer
from python.directories import *
from python.utils.string_utils import *
from python.build import build
from python.thread_handler import ThreadHandler
from python.build_event_handler import ModifiedEventBuildEventHandler
from python.signature_generator import SIGNATURE_IGNORE, SIGNATURE

if __name__ == "__main__":
    # Verify the project structure.
    for dirpath, dirnames, filenames in os.walk("."):
        if any([x in dirpath for x in SIGNATURE_IGNORE]):
            continue
        dir_contents = dirnames
        dir_contents.extend(filenames)
        if (dirpath in SIGNATURE.keys() and not all([x in dir_contents for x in SIGNATURE[dirpath]])):
            print(f"Error: Project signature mismatch at: '{dirpath}' requires: '{SIGNATURE[dirpath]}'.")
            exit()

    # Start SASS watch to compile SCSS into CSS every time there is a change.
    subprocess.Popen(["npx", "sass", "--watch", f"{SCSS_PREBUILD_DIR}:{CSS_PREBUILD_DIR}"], shell=True)

    subprocess.Popen(["npx", "babel", "dev/js/src", "--watch", "--out-file", "dev/js/lib/slate.js"], shell=True)

    # Wait for SASS to complete then build Slate once on run.
    time.sleep(1)
    build()

    exit()

    # Create the event handler to store and handle file modification events in the project.
    event_handler = ModifiedEventBuildEventHandler()
    # Create an observer for file update events.
    observer = Observer()
    # Schedule the event handler to run on events in relevant directories.
    observer.schedule(event_handler, SLATE_DIR)
    observer.schedule(event_handler, HTML_DIR)
    observer.schedule(event_handler, CSS_PREBUILD_DIR)
    observer.schedule(event_handler, CSS_DIR)
    observer.schedule(event_handler, JS_PREBUILD_DIR)
    observer.schedule(event_handler, JS_DIR)
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
