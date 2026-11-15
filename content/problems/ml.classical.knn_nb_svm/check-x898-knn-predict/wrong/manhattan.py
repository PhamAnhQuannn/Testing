import numpy as np


def knn_predict(X_train, y_train, X_test, k):
    # BUG: Manhattan distance instead of Euclidean -> wrong nearest neighbours on some inputs
    Xtr = np.array(X_train, dtype=float)
    ytr = np.array(y_train)
    out = []
    for x in np.array(X_test, dtype=float):
        dist = np.abs(Xtr - x).sum(axis=1)
        order = np.argsort(dist, kind="stable")[:k]
        labels = ytr[order]
        vals, counts = np.unique(labels, return_counts=True)
        out.append(int(vals[counts == counts.max()].min()))
    return out
