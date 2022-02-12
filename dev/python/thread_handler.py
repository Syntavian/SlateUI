from threading import Thread

class ThreadHandler:
    def __init__(self, target) -> None:
        self.rebuild_thread: Thread | None = None
        self.target = target

    def handle_new_build(self) -> None:
        self.stop()
        self.rebuild_thread = Thread(target=self.target)
        self.rebuild_thread.start()

    def stop(self) -> None:
        if self.rebuild_thread: 
            self.rebuild_thread.join()
