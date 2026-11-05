from bisect import bisect_right


class SnapshotArray:
    def __init__(self, length):
        self._hist = [[(0, 0)] for _ in range(length)]
        self._snap = 0

    def set(self, index, val):
        h = self._hist[index]
        if h[-1][0] == self._snap:
            h[-1] = (self._snap, val)
        else:
            h.append((self._snap, val))

    def snap(self):
        self._snap += 1
        return self._snap - 1

    def get(self, index, snap_id):
        h = self._hist[index]
        i = bisect_right(h, (snap_id, float("inf"))) - 1
        return h[i][1]
