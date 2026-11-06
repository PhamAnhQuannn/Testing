class Cart:
    """Cart with int money. Discount is a strategy by name; total() applies it to subtotal."""

    def __init__(self):
        self.lines = []  # (name, price, qty)
        self.kind = "none"

    def add(self, name, price, qty):
        self.lines.append((name, price, qty))

    def set_discount(self, kind):
        self.kind = kind

    def subtotal(self):
        return sum(price * qty for _, price, qty in self.lines)

    def total(self):
        sub = self.subtotal()
        if self.kind == "percent10":
            return sub * 90 // 100
        if self.kind == "fixed50":
            return max(0, sub - 50)
        return sub
