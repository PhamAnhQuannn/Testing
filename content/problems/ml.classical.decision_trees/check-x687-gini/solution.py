def gini(labels):
    n = len(labels)
    if n == 0:
        return 0.0
    counts = {}
    for y in labels:
        counts[y] = counts.get(y, 0) + 1
    impurity = 1.0 - sum((c / n) ** 2 for c in counts.values())
    return round(impurity, 6)
