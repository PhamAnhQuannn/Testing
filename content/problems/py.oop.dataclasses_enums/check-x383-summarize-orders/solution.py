from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    NEW = 1
    PAID = 2
    SHIPPED = 3


@dataclass(frozen=True)
class Order:
    status: Status
    amount: int


def summarize_orders(rows):
    orders = [Order(Status[name], amount) for name, amount in rows]
    out = []
    for s in Status:
        total = sum(o.amount for o in orders if o.status is s)
        out.append(f"{s.name}:{total}")
    out.append(f"distinct:{len(set(orders))}")
    return out
