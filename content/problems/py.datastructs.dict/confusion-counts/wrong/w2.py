def confusion_counts(y_true, y_pred):
    counts = {}
    for t, p in zip(y_true, y_pred, strict=True):
        key = "tp" if t == 1 and p == 1 else "fp" if p == 1 else "fn" if t == 1 else "tn"
        counts[key] = counts.get(key, 0) + 1
    return counts
