import math


def layer_norm(xs):
    n = len(xs)
    mean = sum(xs) / n
    var = sum((x - mean) ** 2 for x in xs) / n
    denom = math.sqrt(var + 1e-5)
    return [round((x - mean) / denom, 6) for x in xs]
