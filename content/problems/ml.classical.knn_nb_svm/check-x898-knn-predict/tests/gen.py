"""Inputs of check-x898-knn-predict; `expected` comes from solution.py (numpy) via gen_hidden.

Tests avoid distance ties (so the k-neighbour set is unambiguous) and include deliberate
vote-tie and Euclidean-vs-Manhattan cases to catch wrong solutions.
"""

SAMPLES = [
    # tree worked example: point (2,2); A(1,2)=1 B(2,3)=0 C(3,2)=1 D(6,6)=0; k=3 -> label 1
    {
        "id": "s1",
        "args": [[[1.0, 2.0], [2.0, 3.0], [3.0, 2.0], [6.0, 6.0]], [1, 0, 1, 0], [[2.0, 2.0]], 3],
    },
    {"id": "s2", "args": [[[0.0, 0.0], [10.0, 10.0]], [0, 1], [[1.0, 1.0], [9.0, 9.0]], 1]},
]

HIDDEN = [
    # k=1 single query
    {"id": "h01", "args": [[[0.0, 0.0], [5.0, 5.0]], [0, 1], [[1.0, 0.5]], 1], "tags": ["edge"]},
    # vote tie at k=2: two nearest carry labels {0,1} -> smallest label 0 wins
    {
        "id": "h02",
        "args": [[[0.0, 0.0], [1.0, 0.0], [10.0, 0.0]], [1, 0, 1], [[0.4, 0.0]], 2],
        "tags": ["edge"],
    },
    # Euclid vs Manhattan disagree on the nearest: from (0,0), B(2,2) euclid 2.83 < A(3,0) euclid 3,
    # but manhattan A 3 < B 4 -> Euclidean picks B's label
    {"id": "h03", "args": [[[3.0, 0.0], [2.0, 2.0]], [0, 1], [[0.0, 0.0]], 1], "tags": []},
    {
        "id": "h04",
        "args": [
            [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [8.0, 8.0], [9.0, 9.0]],
            [0, 0, 1, 1, 1],
            [[2.5, 2.4]],
            3,
        ],
        "tags": [],
    },
    {
        "id": "h05",
        "args": [
            [[0.0, 0.0], [4.0, 0.0], [0.0, 4.0], [4.0, 4.0]],
            [0, 1, 2, 3],
            [[0.3, 0.2], [3.7, 3.8]],
            1,
        ],
        "tags": [],
    },
    {
        "id": "h06",
        "args": [
            [[-2.0, -2.0], [-1.0, 0.0], [1.0, 1.0], [3.0, 2.0]],
            [0, 0, 1, 1],
            [[0.0, 0.0]],
            3,
        ],
        "tags": [],
    },
    {
        "id": "h07",
        "args": [
            [[0.0, 0.0], [1.0, 2.0], [2.0, 1.0], [5.0, 5.0], [6.0, 4.0]],
            [1, 1, 0, 0, 0],
            [[1.2, 1.3], [5.4, 4.6]],
            3,
        ],
        "tags": [],
    },
    # all-same-label neighbourhood
    {
        "id": "h08",
        "args": [[[0.0, 0.0], [0.5, 0.5], [0.9, 0.1]], [2, 2, 2], [[0.4, 0.3]], 3],
        "tags": [],
    },
    # distance tie: (1,0) and (0,1) are both distance 1 from (0,0); k=1 breaks the tie by the
    # smaller training index -> picks (1,0), label 0
    {"id": "h09", "args": [[[1.0, 0.0], [0.0, 1.0]], [0, 1], [[0.0, 0.0]], 1], "tags": []},
]


def _lcg(seed, n):
    """Deterministic random datasets: integer-ish float coords spread to avoid distance ties."""
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        ntr = 4 + (x >> 8) % 6
        xtr, ytr = [], []
        for _ in range(ntr):
            x = (x * 1103515245 + 12345) % 2147483648
            a = float((x >> 8) % 23 - 11)
            x = (x * 1103515245 + 12345) % 2147483648
            b = float((x >> 8) % 23 - 11)
            x = (x * 1103515245 + 12345) % 2147483648
            xtr.append([a, b])
            ytr.append(int((x >> 8) % 3))
        x = (x * 1103515245 + 12345) % 2147483648
        nte = 1 + (x >> 8) % 3
        xte = []
        for _ in range(nte):
            x = (x * 1103515245 + 12345) % 2147483648
            a = float((x >> 8) % 23 - 11) + 0.5
            x = (x * 1103515245 + 12345) % 2147483648
            b = float((x >> 8) % 23 - 11) + 0.3
            xte.append([a, b])
        x = (x * 1103515245 + 12345) % 2147483648
        k = 1 + 2 * ((x >> 8) % ((ntr // 2) or 1))
        k = min(k, ntr)
        out.append([xtr, ytr, xte, k])
    return out


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
