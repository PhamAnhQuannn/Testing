class SeatStore:
    """Optimistic locking model: book is a compare-and-set on the seat version."""

    def __init__(self):
        # seat id -> [version, booked]
        self.seats = {}

    def add(self, seat):
        if seat not in self.seats:
            self.seats[seat] = [0, False]

    def version(self, seat):
        if seat not in self.seats:
            return -1
        return self.seats[seat][0]

    def book(self, seat, expected_version):
        if seat not in self.seats:
            return False
        rec = self.seats[seat]
        if rec[1] or rec[0] != expected_version:
            return False
        rec[1] = True
        rec[0] += 1
        return True

    def is_booked(self, seat):
        if seat not in self.seats:
            return False
        return self.seats[seat][1]
