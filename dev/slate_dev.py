import os
import subprocess
import time

from watchdog.observers import Observer

from python.build import build_app
from python.build_event_handler import ModifiedEventBuildEventHandler
from python.debug import debug
from python.directories import *
from python.signature_generator import SIGNATURE, SIGNATURE_IGNORE
from python.thread_handler import ThreadHandler
from python.utils.string_utils import *


def verify_signature():
    """Verify the project structure"""
    for dirpath, dirnames, filenames in os.walk("."):
        if any([x in dirpath for x in SIGNATURE_IGNORE]):
            continue
        dir_contents = dirnames
        dir_contents.extend(filenames)
        if dirpath in SIGNATURE.keys() and not all(
            [x in dir_contents for x in SIGNATURE[dirpath]]
        ):
            print(
                f"Error: Project signature mismatch at: '{dirpath}' requires: '{SIGNATURE[dirpath]}'."
            )
            exit()


@debug
def build_css():
    """Run SASS to compile SCSS into CSS then format the CSS for Slate to use"""
    subprocess.run(["npx", "sass", "dev/scss:dev/css"], shell=True)


@debug
def build_js():
    """Run SWC to compile TS into JS lib"""
    subprocess.run(["npx", "swc", "./dev/ts", "-d", "./dev/js"], shell=True)
    subprocess.run(["npx", "spack"], shell=True)


if __name__ == "__main__":
    verify_signature()

    build_css()
    build_js()

    build_app()

    exit()

    # Create the event handler to store and handle file modification events in the project
    event_handler = ModifiedEventBuildEventHandler()
    # Create an observer for file update events
    observer = Observer()
    # Schedule the event handler to run on events in relevant directories
    observer.schedule(event_handler, SLATE_DIR)
    observer.schedule(event_handler, HTML_DIR)
    observer.schedule(event_handler, CSS_PREBUILD_DIR)
    observer.schedule(event_handler, CSS_DIR)
    observer.start()
    # Create the thread handler for build threads
    thread_handler = ThreadHandler(build_app)
    try:
        while True:
            time.sleep(1)
            # Call the event handler to run the thread handler every tick if a file event has occurred
            event_handler.update(thread_handler)
    finally:
        observer.stop()
        thread_handler.stop()
        observer.join()
        exit()
