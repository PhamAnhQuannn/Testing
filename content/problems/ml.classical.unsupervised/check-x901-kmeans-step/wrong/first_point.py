import numpy as np


def kmeans_step(xs, centroids):
    # BUG: new centroid is the first assigned point instead of the cluster mean
    x = np.array(xs, dtype=float)
    c = np.array(centroids, dtype=float)
    labels = np.abs(x[:, None] - c[None, :]).argmin(axis=1)
    out = []
    for j in range(len(c)):
        pts = x[labels == j]
        out.append(round(float(pts[0]), 6) if len(pts) else round(float(c[j]), 6))
    return out
