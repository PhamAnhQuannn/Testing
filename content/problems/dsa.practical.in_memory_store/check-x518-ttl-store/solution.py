class TTLStore:
    def __init__(self):
        self._d = {}  # key -> (value, expiry)

    def set(self, key, value, now, ttl):
        self._d[key] = (value, now + ttl)

    def get(self, key, now):
        item = self._d.get(key)
        if item is None:
            return None
        value, expiry = item
        if now >= expiry:
            del self._d[key]
            return None
        return value

    def delete(self, key):
        self._d.pop(key, None)
