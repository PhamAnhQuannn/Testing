import numpy as np


def kmeans_step(xs, centroids):
    x = np.array(xs, dtype=float)
    c = np.array(centroids, dtype=float)
    # assign each point to the nearest centroid; a distance tie goes to the lower index
    labels = np.abs(x[:, None] - c[None, :]).argmin(axis=1)
    out = []
    for j in range(len(c)):
        pts = x[labels == j]
        # empty cluster keeps its old centroid
        out.append(round(float(pts.mean()), 6) if len(pts) else round(float(c[j]), 6))
    return out
