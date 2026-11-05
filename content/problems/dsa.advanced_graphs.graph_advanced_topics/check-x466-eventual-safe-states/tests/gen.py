"""Inputs of check-x466-eventual-safe-states; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[1, 2], [2, 3], [5], [0], [5], [], []]]},
    {"id": "s2", "args": [[[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []]]},
    {"id": "s3", "args": [[[], [0], [1]]]},
]


def _dag(seed, n, deg):
    """Random DAG: edges only go from i to larger j (all nodes safe)."""
    x = seed
    g = []
    for i in range(n):
        row = []
        for _ in range(deg):
            x = (x * 1103515245 + 12345) % 2147483648
            if i + 1 < n:
                row.append(i + 1 + (x >> 8) % (n - i - 1))
        g.append(sorted(set(row)))
    return g


def _random(seed, n, deg):
    """Random digraph (cycles likely); duplicates removed, no self-loops needed."""
    x = seed
    g = []
    for _ in range(n):
        row = set()
        for _ in range(deg):
            x = (x * 1103515245 + 12345) % 2147483648
            row.add((x >> 8) % n)
        g.append(sorted(row))
    return g


def _chain_cycle_tail(n):
    """0 -> 1 -> ... -> n-1 -> 0 : one big cycle, nothing is safe."""
    return [[(i + 1) % n] for i in range(n)]


def _path(n):
    return [[i + 1] if i + 1 < n else [] for i in range(n)]


HIDDEN = [
    {"id": "h01", "args": [[[]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[0]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[], [], [], []]], "tags": ["edge"]},
    {"id": "h04", "args": [_chain_cycle_tail(8)], "tags": []},
    {"id": "h05", "args": [_path(50)], "tags": []},
    {"id": "h06", "args": [_dag(1, 40, 3)], "tags": []},
    {"id": "h07", "args": [_random(2, 30, 1)], "tags": []},
    {"id": "h08", "args": [_random(3, 60, 2)], "tags": []},
    {"id": "h09", "args": [_random(4, 200, 2)], "tags": []},
    {"id": "h10", "args": [_path(3000)], "tags": []},
    {"id": "h11", "args": [_chain_cycle_tail(3000)], "tags": []},
    {"id": "h12", "args": [_random(5, 500, 3)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
