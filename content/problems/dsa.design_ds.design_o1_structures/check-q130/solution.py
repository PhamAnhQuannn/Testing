class MinStack:
    def __init__(self):
        self.s = []

    def push(self, x):
        self.s.append((x, min(x, self.s[-1][1]) if self.s else x))

    def pop(self):
        self.s.pop()

    def top(self):
        return self.s[-1][0]

    def get_min(self):
        return self.s[-1][1]
