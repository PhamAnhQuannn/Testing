from bisect import bisect_right


class HitCounter:
    def __init__(self):
        self._t = []

    def hit(self, timestamp):
        self._t.append(timestamp)

    def get_hits(self, timestamp):
        lo = bisect_right(self._t, timestamp - 300)
        hi = bisect_right(self._t, timestamp)
        return hi - lo
