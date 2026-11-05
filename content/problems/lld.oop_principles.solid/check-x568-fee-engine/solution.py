RATES = {"bike": 1, "car": 2, "truck": 3}


def total_fee(items):
    total = 0
    for kind, base in items:
        total += base * RATES.get(kind, 1)
    return total
