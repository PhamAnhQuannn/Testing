import numpy as np


def knn_predict(X_train, y_train, X_test, k):
    # BUG: on a vote tie picks the LARGEST label instead of the smallest
    Xtr = np.array(X_train, dtype=float)
    ytr = np.array(y_train)
    out = []
    for x in np.array(X_test, dtype=float):
        dist = np.sqrt(((Xtr - x) ** 2).sum(axis=1))
        order = np.argsort(dist, kind="stable")[:k]
        labels = ytr[order]
        vals, counts = np.unique(labels, return_counts=True)
        out.append(int(vals[counts == counts.max()].max()))
    return out
