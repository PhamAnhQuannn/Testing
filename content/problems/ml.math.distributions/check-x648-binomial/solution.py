import math


def binomial_pmf(n, k, p):
    if k < 0 or k > n:
        return 0.0
    return float(round(math.comb(n, k) * p**k * (1 - p) ** (n - k), 6))
