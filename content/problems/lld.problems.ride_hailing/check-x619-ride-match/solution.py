class RideSystem:
    """Nearest-driver matching on a 1-D line. Failure is a -1 sentinel."""

    def __init__(self):
        self.pos = {}  # driver_id -> position
        self.free = {}  # driver_id -> True if available

    def add_driver(self, driver_id, pos):
        self.pos[driver_id] = pos
        self.free[driver_id] = True

    def request(self, rider_pos):
        best = -1
        best_dist = 0
        for did in sorted(self.pos):
            if not self.free[did]:
                continue
            dist = abs(self.pos[did] - rider_pos)
            if best == -1 or dist < best_dist:
                best = did
                best_dist = dist
        if best != -1:
            self.free[best] = False
        return best

    def complete(self, driver_id):
        if driver_id in self.free:
            self.free[driver_id] = True

    def available_count(self):
        return sum(1 for did in sorted(self.free) if self.free[did])
