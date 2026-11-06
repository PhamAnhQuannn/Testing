import math


def predict_proba(weights, bias, x):
    z = bias + sum(w * xi for w, xi in zip(weights, x))
    if z >= 0:
        p = 1.0 / (1.0 + math.exp(-z))
    else:
        e = math.exp(z)
        p = e / (1.0 + e)
    return round(p, 6)
