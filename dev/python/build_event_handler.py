from watchdog.events import FileSystemEventHandler
from python.thread_handler import ThreadHandler


class ModifiedEventBuildEventHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        super().__init__()
        self.event_batch = set()

    def on_modified(self, event):
        self.event_batch.add(event)

    def update(self, thread_handler: ThreadHandler):
        if len(self.event_batch) != 0:
            print("\nChanges in:", end=' ')
            [print(v.src_path[v.src_path.rindex('/') + 1:], end=' ')
             for v in self.event_batch]
            print('\n')
            thread_handler.handle_new_build()
        self.event_batch.clear()
