class BoundedBuffer:
    def __init__(self, capacity):
        self._cap = capacity
        self._items = []

    def put(self, x):
        if len(self._items) >= self._cap:
            return False
        self._items.append(x)
        return True

    def get(self):
        if not self._items:
            return None
        return self._items.pop(0)

    def size(self):
        return len(self._items)
