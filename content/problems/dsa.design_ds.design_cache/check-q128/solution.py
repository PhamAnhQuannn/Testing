class MyHashMap:
    def __init__(self):
        self.b = [[] for _ in range(97)]

    def put(self, k, v):
        row = self.b[k % 97]
        for p in row:
            if p[0] == k:
                p[1] = v
                return
        row.append([k, v])

    def get(self, k):
        for a, v in self.b[k % 97]:
            if a == k:
                return v
        return -1

    def remove(self, k):
        self.b[k % 97] = [p for p in self.b[k % 97] if p[0] != k]
