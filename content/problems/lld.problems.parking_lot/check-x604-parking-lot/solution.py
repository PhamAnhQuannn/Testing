class ParkingLot:
    """Two spot types, ticket ids 1,2,3..., fee = hours * rate. Failure is a -1 sentinel."""

    RATES = {"car": 20, "moto": 10}

    def __init__(self, car_spots, moto_spots):
        self.free = {"car": car_spots, "moto": moto_spots}
        self.tickets = {}  # ticket_id -> kind of the vehicle still parked
        self.next_id = 1

    def park(self, kind):
        if self.free.get(kind, 0) <= 0:
            return -1
        self.free[kind] -= 1
        tid = self.next_id
        self.next_id += 1
        self.tickets[tid] = kind
        return tid

    def leave(self, ticket_id, hours):
        kind = self.tickets.pop(ticket_id, None)
        if kind is None:
            return -1
        self.free[kind] += 1
        return hours * self.RATES[kind]

    def available(self, kind):
        return self.free.get(kind, 0)
