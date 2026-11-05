class BookingSystem:
    """Seat booking that prevents double-booking: check free, then mark booked."""

    def __init__(self):
        # seat id -> booked flag (True = booked)
        self.seats = {}

    def add_seat(self, seat):
        if seat not in self.seats:
            self.seats[seat] = False

    def book(self, seat):
        if seat not in self.seats or self.seats[seat]:
            return False
        self.seats[seat] = True
        return True

    def cancel(self, seat):
        if not self.seats.get(seat, False):
            return False
        self.seats[seat] = False
        return True

    def is_booked(self, seat):
        return self.seats.get(seat, False)

    def free_count(self):
        return sum(1 for booked in self.seats.values() if not booked)
