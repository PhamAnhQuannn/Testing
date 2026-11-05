class Underground:
    def __init__(self):
        self.on = {}
        self.tot = {}

    def check_in(self, i, s, t):
        self.on[i] = (s, t)

    def check_out(self, i, s, t):
        a, t0 = self.on.pop(i)
        k = (a, s)
        x = self.tot.get(k, (0, 0))
        self.tot[k] = (x[0] + t - t0, x[1] + 1)

    def average(self, a, b):
        x = self.tot[a, b]
        return x[0] / x[1]
