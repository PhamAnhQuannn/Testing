def r_squared(y_true, y_pred):
    n = len(y_true)
    if n == 0:
        return 0.0
    mean = sum(y_true) / n
    ss_tot = sum((t - mean) ** 2 for t in y_true)
    if ss_tot == 0:
        return 0.0
    ss_res = sum((t - p) ** 2 for t, p in zip(y_true, y_pred))
    return float(round(1 - ss_res / ss_tot, 6))
