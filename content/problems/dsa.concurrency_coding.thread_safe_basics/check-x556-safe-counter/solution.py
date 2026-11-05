class SafeCounter:
    """Lock-protected counter modeled sequentially: each op is one atomic critical section."""

    def __init__(self):
        self._n = 0

    def incr(self):
        self._n += 1

    def add(self, n):
        self._n += n

    def value(self):
        return self._n
