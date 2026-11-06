def expectation_variance(xs, ps):
    e = sum(x * p for x, p in zip(xs, ps))
    var = sum(p * (x - e) ** 2 for x, p in zip(xs, ps))
    return [float(round(e, 6)), float(round(var, 6))]
