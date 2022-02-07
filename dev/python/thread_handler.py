import threading

class ThreadHandler:
    def __init__(self, target):
        self.rebuild_thread = None
        self.target = target

    def handle_new_build(self):
        if self.rebuild_thread:
            self.rebuild_thread.join()
        self.rebuild_thread = threading.Thread(target=self.target)
        self.rebuild_thread.start()
