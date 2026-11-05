_MISSING = object()


class TxnStore:
    def __init__(self):
        self._d = {}
        self._undo = []  # stack of {key: previous value or _MISSING}

    def set(self, key, value):
        if self._undo:
            self._undo[-1].setdefault(key, self._d.get(key, _MISSING))
        self._d[key] = value

    def get(self, key):
        return self._d.get(key)

    def begin(self):
        self._undo.append({})

    def commit(self):
        if not self._undo:
            return False
        frame = self._undo.pop()
        if self._undo:
            for k, old in frame.items():
                self._undo[-1].setdefault(k, old)
        return True

    def rollback(self):
        if not self._undo:
            return False
        frame = self._undo.pop()
        for k, old in frame.items():
            if old is _MISSING:
                self._d.pop(k, None)
            else:
                self._d[k] = old
        return True
