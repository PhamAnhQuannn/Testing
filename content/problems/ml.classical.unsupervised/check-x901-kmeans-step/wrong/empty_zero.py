import numpy as np


def kmeans_step(xs, centroids):
    # BUG: an empty cluster is set to 0.0 instead of keeping its old centroid
    x = np.array(xs, dtype=float)
    c = np.array(centroids, dtype=float)
    labels = np.abs(x[:, None] - c[None, :]).argmin(axis=1)
    out = []
    for j in range(len(c)):
        pts = x[labels == j]
        out.append(round(float(pts.mean()), 6) if len(pts) else 0.0)
    return out
