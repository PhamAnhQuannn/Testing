import math


def entropy(probs):
    total = 0.0
    for p in probs:
        if p == 0:
            continue
        total -= p * math.log2(p)
    return float(round(total, 6))
