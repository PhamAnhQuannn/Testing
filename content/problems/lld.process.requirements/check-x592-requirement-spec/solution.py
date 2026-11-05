class RequirementSpec:
    """Records requirements by kind and the in-scope / out-of-scope items."""

    def __init__(self):
        self._counts = {"functional": 0, "nonfunctional": 0}
        self._in = []
        self._out = []

    def add(self, kind, text):
        self._counts[kind] += 1

    def set_scope(self, text, inside):
        if inside:
            self._in.append(text)
        else:
            self._out.append(text)

    def count(self, kind):
        return self._counts[kind]

    def in_scope(self):
        return sorted(self._in)
