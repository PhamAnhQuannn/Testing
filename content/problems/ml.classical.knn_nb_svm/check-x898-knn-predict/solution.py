import numpy as np


def knn_predict(X_train, y_train, X_test, k):
    Xtr = np.array(X_train, dtype=float)
    ytr = np.array(y_train)
    out = []
    for x in np.array(X_test, dtype=float):
        dist = np.sqrt(((Xtr - x) ** 2).sum(axis=1))
        # nearest k by distance ascending, ties broken by smaller row index (stable sort)
        order = np.argsort(dist, kind="stable")[:k]
        labels = ytr[order]
        vals, counts = np.unique(labels, return_counts=True)
        # majority vote; on a vote tie pick the smallest label
        best = vals[counts == counts.max()].min()
        out.append(int(best))
    return out
