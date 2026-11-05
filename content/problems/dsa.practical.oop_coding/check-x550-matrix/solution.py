class Matrix:
    def __init__(self, rows, cols):
        self._r = rows
        self._c = cols
        self._d = {}

    def set(self, r, c, v):
        self._d[(r, c)] = v

    def get(self, r, c):
        return self._d.get((r, c), 0)

    def transpose(self):
        self._d = {(c, r): v for (r, c), v in self._d.items()}
        self._r, self._c = self._c, self._r

    def dims(self):
        return [self._r, self._c]
