def mse(y_true, y_pred):
    n = len(y_true)
    if n == 0:
        return 0.0
    return float(round(sum((p - t) ** 2 for t, p in zip(y_true, y_pred)) / n, 6))
