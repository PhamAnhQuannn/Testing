class TimeMap:
    def __init__(self):
        self.d = {}

    def set(self, k, v, t):
        self.d.setdefault(k, []).append((t, v))

    def get(self, k, t):
        import bisect

        a = self.d.get(k, [])
        i = bisect.bisect_right(a, (t, chr(1114111)))
        return a[i - 1][1] if i else ""
