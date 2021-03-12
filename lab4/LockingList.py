import threading


class LockingList:
    items: list[object] = None
    lock_object: threading.Lock = None

    def __init__(self):
        self.items = []
        self.lock_object = threading.Lock()

    def is_empty(self) -> bool:
        return self.items == []

    def append(self, item) -> None:
        with self.lock_object:
            self.items.append(item)

    def remove(self, item) -> object:
        with self.lock_object:
            return self.items.remove(item)

    def remove(self) -> object:
        with self.lock_object:
            return self.items.pop()

    def peek(self) -> object:
        return self.items[-1]

    def size(self) -> int:
        return len(self.items)

    def contains(self, item) -> bool:
        return item in self.items

    def __delitem__(self, key) -> bool:
        with self.lock_object:
            return self.__delitem__(key)

    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

    def __iter__(self):
        return self.items.__iter__()
