import math


def _cosine(u, v):
    nu = math.sqrt(sum(x * x for x in u))
    nv = math.sqrt(sum(x * x for x in v))
    if nu == 0 or nv == 0:
        return 0.0
    return sum(x * y for x, y in zip(u, v)) / (nu * nv)


def most_similar(query, items):
    best = -1
    best_s = None
    for i, v in enumerate(items):
        s = _cosine(query, v)
        if best_s is None or s > best_s:
            best = i
            best_s = s
    return best
