"""Inputs of check-x844-tree-depth; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[1, 0], [2, 1], [3, 1], [4, 2]]]},
    {"id": "s2", "args": [[[3, 1], [1, 0], [2, 1], [5, 3], [4, 5]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[[1, 0]]], "tags": ["edge", "single"]},
    {"id": "h03", "args": [[[7, 1]]], "tags": ["edge", "single", "absent-init"]},
    {
        "id": "h04",
        "args": [[[1, 0], [2, 1], [3, 2], [4, 3], [5, 4]]],
        "tags": ["linear-chain"],
    },
    {
        "id": "h05",
        "args": [[[5, 4], [4, 3], [3, 2], [2, 1], [1, 0]]],
        "tags": ["linear-chain", "reverse-order"],
    },
    {
        "id": "h06",
        "args": [[[1, 0], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1]]],
        "tags": ["wide-shallow"],
    },
    {
        "id": "h07",
        "args": [[[1, 0], [2, 1], [3, 1], [4, 2], [5, 2], [6, 3], [7, 3]]],
        "tags": ["balanced"],
    },
    {
        "id": "h08",
        "args": [[[10, 1], [11, 10], [12, 10], [13, 12]]],
        "tags": ["absent-init"],
    },
    {
        "id": "h09",
        "args": [[[20, 5], [30, 20], [40, 30], [50, 20]]],
        "tags": ["absent-init", "out-of-order"],
    },
    {
        "id": "h10",
        "args": [[[9, 8], [8, 7], [7, 0], [6, 7], [5, 6], [4, 5], [3, 9]]],
        "tags": ["unsorted", "deep-branch"],
    },
    {
        "id": "h11",
        "args": [[[2, 0], [1, 2], [3, 1], [4, 2]]],
        "tags": ["root-not-smallest"],
    },
    {
        "id": "h12",
        "args": [[[100, 0], [200, 100], [300, 100], [400, 300], [500, 400], [600, 200]]],
        "tags": ["large-pids"],
    },
]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        count = (x >> 8) % 9
        edges = []
        if count:
            # distinct increasing pids; first pid >= 2 so ppid 1 can be an absent init
            x = _next(x)
            pids = [2 + (x >> 8) % 3]
            for _i in range(count - 1):
                x = _next(x)
                pids.append(pids[-1] + 1 + (x >> 8) % 3)
            x = _next(x)
            root_ppid = 0 if (x >> 8) % 3 else 1
            edges.append([pids[0], root_ppid])
            for k in range(1, count):
                x = _next(x)
                edges.append([pids[k], pids[(x >> 8) % k]])
            # shuffle (Fisher-Yates)
            for i in range(len(edges) - 1, 0, -1):
                x = _next(x)
                j = (x >> 8) % (i + 1)
                edges[i], edges[j] = edges[j], edges[i]
        out.append([edges])
    return out


for _i, _a in enumerate(_lcg(43, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
