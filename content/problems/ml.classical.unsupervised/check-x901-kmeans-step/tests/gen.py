"""Inputs of check-x901-kmeans-step; `expected` comes from solution.py (numpy) via gen_hidden.

1-D k-means, one iteration. Cases include empty clusters (kept at old centroid) and even-count
clusters (mean != median) to catch wrong solutions.
"""

SAMPLES = [
    # tree worked example: points 1,2,3,10,11,12 with centroids 1,2 -> 1.0 and 7.6 after one step
    {"id": "s1", "args": [[1.0, 2.0, 3.0, 10.0, 11.0, 12.0], [1.0, 2.0]]},
    # c2 (=20) gets no points -> kept
    {"id": "s2", "args": [[0.0, 10.0], [0.0, 5.0, 20.0]]},
]

HIDDEN = [
    {"id": "h01", "args": [[5.0], [0.0, 10.0]], "tags": ["edge"]},  # empty cluster kept
    {
        "id": "h02",
        "args": [[1.0, 2.0, 3.0, 4.0], [1.0, 4.0]],
        "tags": [],
    },  # even clusters, mean!=median
    {"id": "h03", "args": [[0.0, 1.0, 8.0, 9.0, 10.0], [0.0, 9.0]], "tags": []},
    {"id": "h04", "args": [[-5.0, -4.0, 4.0, 5.0], [-4.5, 4.5]], "tags": []},
    {"id": "h05", "args": [[2.0, 2.0, 2.0], [0.0, 100.0]], "tags": ["edge"]},  # one cluster empty
    {"id": "h06", "args": [[1.0, 3.0, 5.0, 7.0, 9.0], [2.0, 6.0, 10.0]], "tags": []},
    {"id": "h07", "args": [[0.5, 1.5, 10.5, 11.5], [1.0, 11.0]], "tags": []},
    {"id": "h08", "args": [[-10.0, 0.0, 10.0, 20.0], [-10.0, 20.0]], "tags": []},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        npts = 3 + (x >> 8) % 8
        pts = []
        for _ in range(npts):
            x = (x * 1103515245 + 12345) % 2147483648
            pts.append(float((x >> 8) % 41 - 20))
        x = (x * 1103515245 + 12345) % 2147483648
        kc = 2 + (x >> 8) % 3
        cents = []
        for _ in range(kc):
            x = (x * 1103515245 + 12345) % 2147483648
            cents.append(float((x >> 8) % 41 - 20) + 0.5)
        out.append([pts, cents])
    return out


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
