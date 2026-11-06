import math


def nll_bernoulli(ys, ps):
    eps = 1e-12
    total = 0.0
    for y, p in zip(ys, ps):
        p = min(max(p, eps), 1 - eps)
        total += y * math.log(p) + (1 - y) * math.log(1 - p)
    return float(round(-total, 6))
