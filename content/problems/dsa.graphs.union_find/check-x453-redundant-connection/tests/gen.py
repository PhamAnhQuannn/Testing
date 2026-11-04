"""Inputs of check-x453-redundant-connection; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[1, 2], [1, 3], [2, 3]]]},
    {"id": "s2", "args": [[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]]},
    {"id": "s3", "args": [[[1, 2], [2, 3], [1, 3]]]},
]


def _graph(seed, n):
    """A random tree on 1..n plus one extra non-duplicate edge, shuffled by a seeded LCG."""
    state = [seed]

    def rnd(bound):
        state[0] = (state[0] * 1103515245 + 12345) % 2147483648
        return (state[0] >> 8) % bound

    edges = [[rnd(i - 1) + 1, i] for i in range(2, n + 1)]
    present = {(min(e), max(e)) for e in edges}
    while True:
        a, b = rnd(n) + 1, rnd(n) + 1
        if a != b and (min(a, b), max(a, b)) not in present:
            edges.append([a, b])
            break
    for i in range(len(edges) - 1, 0, -1):
        j = rnd(i + 1)
        edges[i], edges[j] = edges[j], edges[i]
    return edges


def _path_plus(n, a, b):
    return [[i, i + 1] for i in range(1, n)] + [[a, b]]


HIDDEN = [
    {"id": "h01", "args": [[[2, 1], [3, 2], [3, 1]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[1, 2], [2, 3], [3, 1]]], "tags": ["edge"]},
    {"id": "h03", "args": [_path_plus(6, 1, 6)], "tags": []},
    {"id": "h04", "args": [_path_plus(6, 3, 5)], "tags": []},
    {"id": "h05", "args": [[[2, 1], [3, 1], [4, 1], [3, 4]]], "tags": []},
    {"id": "h06", "args": [_graph(1, 8)], "tags": []},
    {"id": "h07", "args": [_graph(2, 15)], "tags": []},
    {"id": "h08", "args": [_graph(3, 40)], "tags": []},
    {"id": "h09", "args": [_graph(4, 200)], "tags": []},
    {"id": "h10", "args": [_path_plus(1000, 1, 1000)], "tags": []},
    {"id": "h11", "args": [_graph(5, 1000)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
