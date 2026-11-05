class ShoppingCart:
    def __init__(self):
        self._lines = {}

    def add(self, item, price, qty):
        if item in self._lines:
            self._lines[item][1] += qty
        else:
            self._lines[item] = [price, qty]

    def remove(self, item):
        self._lines.pop(item, None)

    def total(self):
        return sum(p * q for p, q in self._lines.values())
