def ece(bins):
    total = sum(b[0] for b in bins)
    if total == 0:
        return 0.0
    return float(round(sum((n / total) * abs(acc - conf) for n, conf, acc in bins), 6))
