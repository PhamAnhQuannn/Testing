def precision_recall_f1(y_true, y_pred):
    n = len(y_true)
    acc = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == p) / n if n else 0.0
    return {"precision": round(acc, 3), "recall": round(acc, 3), "f1": round(acc, 3)}
