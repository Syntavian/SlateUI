import subprocess
import time
from watchdog.observers import Observer
from python.directories import *
from python.string_utils import *
from python.build import build
from python.thread_handler import ThreadHandler
from python.build_event_handler import ModifiedEventBuildEventHandler

if __name__ == "__main__":
    thread_handler = ThreadHandler(build)
    subprocess.Popen(["sass", "--watch", "dev\scss:dev\css"])
    time.sleep(1)
    build()
    event_handler = ModifiedEventBuildEventHandler()
    observer = Observer()
    observer.schedule(event_handler, CSS_PREBUILD_DIR)
    observer.start()
    try:
        while True:
            time.sleep(1)
            event_handler.update(thread_handler)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    exit()
