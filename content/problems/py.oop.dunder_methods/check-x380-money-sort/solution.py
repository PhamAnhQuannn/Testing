def rank_money(cents):
    """Sort Money objects ascending and append their total."""

    class Money:
        def __init__(self, xu):
            self.xu = xu

        def __lt__(self, other):
            return self.xu < other.xu

        def __add__(self, other):
            return Money(self.xu + other.xu)

        def __str__(self):
            return f"{self.xu // 100}.{self.xu % 100:02d}"

    items = [Money(c) for c in cents]
    total = Money(0)
    for m in items:
        total = total + m
    return [str(m) for m in sorted(items)] + [str(total)]
