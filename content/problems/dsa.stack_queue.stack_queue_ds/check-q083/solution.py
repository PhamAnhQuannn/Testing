class MyQueue:
    def __init__(self):
        self.a, self.b = ([], [])

    def push(self, x):
        self.a.append(x)

    def _move(self):
        if not self.b:
            while self.a:
                self.b.append(self.a.pop())

    def pop(self):
        self._move()
        return self.b.pop()

    def peek(self):
        self._move()
        return self.b[-1]

    def empty(self):
        return not self.a and (not self.b)
