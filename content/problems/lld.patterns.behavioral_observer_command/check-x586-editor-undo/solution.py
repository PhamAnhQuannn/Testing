class _TypeCommand:
    """Command: append text; undo removes exactly that many characters."""

    def __init__(self, s):
        self.s = s

    def execute(self, text):
        return text + self.s

    def undo(self, text):
        return text[: len(text) - len(self.s)]


class _DeleteCommand:
    """Command: remove the last n characters (clamped); remembers what it removed."""

    def __init__(self, n):
        self.n = n
        self.removed = ""

    def execute(self, text):
        k = min(max(self.n, 0), len(text))
        self.removed = text[len(text) - k :]
        return text[: len(text) - k]

    def undo(self, text):
        return text + self.removed


class Editor:
    def __init__(self):
        self._text = ""
        self._history = []

    def _run(self, cmd):
        self._text = cmd.execute(self._text)
        self._history.append(cmd)

    def type(self, s):
        self._run(_TypeCommand(s))

    def delete(self, n):
        self._run(_DeleteCommand(n))

    def undo(self):
        if self._history:
            self._text = self._history.pop().undo(self._text)

    def text(self):
        return self._text
