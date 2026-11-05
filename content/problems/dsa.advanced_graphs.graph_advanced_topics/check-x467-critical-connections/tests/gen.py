"""Inputs of check-x467-critical-connections; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [4, [[0, 1], [1, 2], [2, 0], [1, 3]]]},
    {"id": "s2", "args": [2, [[0, 1]]]},
    {"id": "s3", "args": [5, [[0, 1], [1, 2], [2, 3], [3, 4]]]},
]


def _chain(n):
    return [[i, i + 1] for i in range(n - 1)]


def _cycle(n):
    return [[i, (i + 1) % n] for i in range(n)]


def _random_connected(seed, n, extra):
    """Random spanning tree plus `extra` additional edges (no duplicates, no self-loops)."""
    x = seed
    seen = set()
    edges = []
    for v in range(1, n):
        x = (x * 1103515245 + 12345) % 2147483648
        u = (x >> 8) % v
        seen.add((u, v))
        edges.append([u, v] if (x >> 4) % 2 else [v, u])
    tries = 0
    while extra > 0 and tries < 10 * n + 50:
        tries += 1
        x = (x * 1103515245 + 12345) % 2147483648
        a = (x >> 8) % n
        x = (x * 1103515245 + 12345) % 2147483648
        b = (x >> 8) % n
        if a == b:
            continue
        key = (min(a, b), max(a, b))
        if key in seen:
            continue
        seen.add(key)
        edges.append([a, b])
        extra -= 1
    return edges


def _two_cycles_bridge():
    return [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 5], [5, 3]]


HIDDEN = [
    {"id": "h01", "args": [1, []], "tags": ["edge"]},
    {"id": "h02", "args": [2, [[1, 0]]], "tags": ["edge"]},
    {"id": "h03", "args": [3, _cycle(3)], "tags": ["edge"]},
    {"id": "h04", "args": [6, _two_cycles_bridge()], "tags": []},
    {"id": "h05", "args": [50, _cycle(50)], "tags": ["edge"]},
    {"id": "h06", "args": [40, _random_connected(1, 40, 5)], "tags": []},
    {"id": "h07", "args": [100, _random_connected(2, 100, 30)], "tags": []},
    {"id": "h08", "args": [300, _random_connected(3, 300, 20)], "tags": []},
    {"id": "h09", "args": [2000, _random_connected(4, 2000, 300)], "tags": []},
    {"id": "h10", "args": [3000, _chain(3000)], "tags": []},
    {"id": "h11", "args": [3000, _cycle(3000)], "tags": []},
    {"id": "h12", "args": [10, [[0, 1], [1, 2], [3, 4]]], "tags": ["edge"]},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
