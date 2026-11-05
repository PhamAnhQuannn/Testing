class NoDiscount:
    def apply(self, subtotal):
        return subtotal


class PercentTen:
    def apply(self, subtotal):
        return subtotal * 90 // 100


class FixedFifty:
    def apply(self, subtotal):
        return max(0, subtotal - 50)


STRATEGIES = {"none": NoDiscount, "percent10": PercentTen, "fixed50": FixedFifty}


class Cart:
    """Context: holds the current discount strategy and delegates the maths to it."""

    def __init__(self):
        self._subtotal = 0
        self._discount = NoDiscount()

    def add(self, price):
        self._subtotal += price

    def set_discount(self, kind):
        self._discount = STRATEGIES[kind]()

    def total(self):
        return self._discount.apply(self._subtotal)
