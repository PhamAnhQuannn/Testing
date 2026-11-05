class TTLCache:
    def __init__(self, ttl):
        self.ttl = ttl
        self.d = {}

    def put(self, k, v, now):
        self.d[k] = (v, now)

    def get(self, k, now):
        if k not in self.d:
            return None
        v, t = self.d[k]
        if now - t >= self.ttl:
            del self.d[k]
            return None
        return v
