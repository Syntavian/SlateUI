import threading

class ThreadHandler:
    def __init__(self, target):
        self.recompile_thread = None
        self.target = target

    def handle_new_compile(self):
        if self.recompile_thread:
            self.recompile_thread.join()
        self.recompile_thread = threading.Thread(target=self.target)
        self.recompile_thread.start()
