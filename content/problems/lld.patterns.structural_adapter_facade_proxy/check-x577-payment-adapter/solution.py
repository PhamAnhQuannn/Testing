class _LegacyGateway:
    """Legacy system: only understands cents."""

    def __init__(self):
        self.cents = 0

    def make_payment(self, cents):
        self.cents += cents

    def make_refund(self, cents):
        self.cents = max(0, self.cents - cents)


class PaymentAdapter:
    """Adapter: new interface pay(amount in whole units) -> legacy make_payment(cents)."""

    def __init__(self):
        self._legacy = _LegacyGateway()

    def pay(self, amount):
        self._legacy.make_payment(amount * 100)

    def total_cents(self):
        return self._legacy.cents

    def refund(self, amount):
        self._legacy.make_refund(amount * 100)
