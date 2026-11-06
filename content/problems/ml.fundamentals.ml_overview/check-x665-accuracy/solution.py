def accuracy(y_true, y_pred):
    n = len(y_true)
    if n == 0:
        return 0.0
    hits = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return float(round(hits / n, 6))
