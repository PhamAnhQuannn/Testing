class Elevator:
    """Single elevator with LOOK scheduling. Next floor always chosen from sorted pending."""

    def __init__(self, start):
        self.floor = start
        self.direction = 1
        self.wanted = set()

    def request(self, floor):
        if floor != self.floor:
            self.wanted.add(floor)

    def step(self):
        if not self.wanted:
            return self.floor
        ordered = sorted(self.wanted)
        above = [f for f in ordered if f > self.floor]
        below = [f for f in ordered if f < self.floor]
        if self.direction == 1 and not above:
            self.direction = -1
        elif self.direction == -1 and not below:
            self.direction = 1
        nxt = above[0] if self.direction == 1 else below[-1]
        self.wanted.discard(nxt)
        self.floor = nxt
        return nxt

    def current(self):
        return self.floor

    def pending(self):
        return sorted(self.wanted)
