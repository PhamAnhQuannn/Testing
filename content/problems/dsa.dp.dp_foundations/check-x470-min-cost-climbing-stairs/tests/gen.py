"""Inputs of check-x470-min-cost-climbing-stairs; expected comes from solution.py."""

SAMPLES = [
    {"id": "s1", "args": [[10, 15, 20]]},
    {"id": "s2", "args": [[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]]},
    {"id": "s3", "args": [[0, 0, 0, 0]]},
]


def _costs(seed, n, hi):
    """Seeded LCG list of `n` costs in [0, hi]."""
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((x >> 8) % (hi + 1))
    return out


HIDDEN = [
    {"id": "h01", "args": [[5, 3]], "tags": ["edge"]},
    {"id": "h02", "args": [[0, 0]], "tags": ["edge"]},
    {"id": "h03", "args": [[7, 7, 7]], "tags": []},
    {"id": "h04", "args": [[999, 0, 999, 0, 999]], "tags": []},
    {"id": "h05", "args": [[1, 2, 3, 4, 5, 6]], "tags": []},
    {"id": "h06", "args": [_costs(1, 10, 20)], "tags": []},
    {"id": "h07", "args": [_costs(2, 25, 999)], "tags": []},
    {"id": "h08", "args": [_costs(3, 100, 50)], "tags": []},
    {"id": "h09", "args": [[999] * 1000], "tags": ["edge"]},
    {"id": "h10", "args": [_costs(4, 1000, 999)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
