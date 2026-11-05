class VendingMachine:
    """Slots dict: code -> [qty, price]; money is int."""

    def __init__(self):
        self._slots = {}
        self._balance = 0

    def load(self, code, qty, price):
        self._slots[code] = [qty, price]

    def insert(self, amount):
        self._balance += amount

    def select(self, code):
        slot = self._slots.get(code)
        if slot is None or slot[0] <= 0 or self._balance < slot[1]:
            return -1
        slot[0] -= 1
        change = self._balance - slot[1]
        self._balance = 0
        return change

    def balance(self):
        return self._balance
