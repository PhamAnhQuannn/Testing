def precision_recall_f1(y_true, y_pred):
    tp = fp = fn = 0
    for t, p in zip(y_true, y_pred, strict=True):
        if p == 1 and t == 1:
            tp += 1
        elif p == 1:
            fp += 1
        elif t == 1:
            fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)
    return {"precision": round(precision, 3), "recall": round(recall, 3), "f1": round(f1, 3)}
