class TokenBucket:
    def __init__(self, capacity, refill_per_sec):
        self.capacity = capacity
        self.rate = refill_per_sec
        self.tokens = capacity
        self.last = None

    def allow(self, timestamp, cost):
        if self.last is not None:
            self.tokens = min(self.capacity, self.tokens + self.rate * (timestamp - self.last))
        self.last = timestamp
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False
