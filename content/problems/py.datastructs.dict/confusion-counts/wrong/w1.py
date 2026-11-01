def confusion_counts(y_true, y_pred):
    counts = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    for t, p in zip(y_true, y_pred, strict=True):
        if t == 1 and p == 1:
            counts["tp"] += 1
        elif t == 0 and p == 1:
            counts["fn"] += 1
        elif t == 1 and p == 0:
            counts["fp"] += 1
        else:
            counts["tn"] += 1
    return counts
