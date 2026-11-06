def prf(y_true, y_pred):
    tp = sum((1 for a, b in zip(y_true, y_pred) if a == 1 and b == 1))
    fp = sum((1 for a, b in zip(y_true, y_pred) if a == 0 and b == 1))
    fn = sum((1 for a, b in zip(y_true, y_pred) if a == 1 and b == 0))
    p = tp / (tp + fp) if tp + fp else 0
    r = tp / (tp + fn) if tp + fn else 0
    f = 2 * p * r / (p + r) if p + r else 0
    return (round(p, 2), round(r, 2), round(f, 2))
