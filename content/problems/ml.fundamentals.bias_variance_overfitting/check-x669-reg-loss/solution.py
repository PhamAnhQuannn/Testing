def reg_loss(base, weights, lam, kind):
    if kind == "l2":
        penalty = lam * sum(w * w for w in weights)
    elif kind == "l1":
        penalty = lam * sum(abs(w) for w in weights)
    else:
        penalty = 0.0
    return float(round(base + penalty, 6))
