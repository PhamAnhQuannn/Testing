import math


def attention_weights(query, keys):
    scores = [sum(q * k for q, k in zip(query, key)) for key in keys]
    m = max(scores)
    exps = [math.exp(s - m) for s in scores]
    total = sum(exps)
    return [round(e / total, 6) for e in exps]
