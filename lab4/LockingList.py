import threading


class LockingList:
    items: list[object] = None
    lock_object: threading.Lock = None

    def __init__(self):
        self.items = []
        self.lock_object = threading.Lock()

    def append(self, item) -> None:
        with self.lock_object:
            self.items.append(item)

    def remove(self, item) -> object:
        with self.lock_object:
            return self.items.remove(item)
