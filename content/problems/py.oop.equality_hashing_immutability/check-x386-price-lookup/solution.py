from dataclasses import FrozenInstanceError, dataclass


@dataclass(frozen=True)
class Money:
    amount: int
    cur: str


def price_lookup(entries, queries):
    table = {}
    for amount, cur, label in entries:
        table[Money(amount, cur)] = label
    labels = [table.get(Money(a, c)) for a, c in queries]
    frozen = False
    try:
        Money(1, "X").amount = 0
    except FrozenInstanceError:
        frozen = True
    return [labels, frozen]
