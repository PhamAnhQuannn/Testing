from collections import deque


class SlidingWindowLimiter:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.q = deque()

    def allow(self, timestamp):
        while self.q and self.q[0] <= timestamp - self.window:
            self.q.popleft()
        if len(self.q) < self.limit:
            self.q.append(timestamp)
            return True
        return False
