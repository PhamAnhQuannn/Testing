"""Inputs of check-x481-unique-paths; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [3, 7]},
    {"id": "s2", "args": [3, 2]},
    {"id": "s3", "args": [2, 2]},
]


def _dims(seed, count, hi):
    """Seeded LCG list of (m, n) pairs in 1..hi."""
    out = []
    x = seed
    for _ in range(count):
        x = (x * 1103515245 + 12345) % 2147483648
        m = (x >> 8) % hi + 1
        x = (x * 1103515245 + 12345) % 2147483648
        n = (x >> 8) % hi + 1
        out.append([m, n])
    return out


HIDDEN = [
    {"id": "h01", "args": [1, 1], "tags": ["edge"]},
    {"id": "h02", "args": [1, 9], "tags": ["edge"]},
    {"id": "h03", "args": [9, 1], "tags": ["edge"]},
    {"id": "h04", "args": [2, 3], "tags": []},
    {"id": "h05", "args": [7, 3], "tags": []},
    {"id": "h06", "args": [10, 10], "tags": []},
    {"id": "h07", "args": [18, 18], "tags": []},
    {"id": "h08", "args": [23, 12], "tags": []},
]
for _i, _a in enumerate(_dims(7, 4, 30)):
    HIDDEN.append({"id": f"h{9 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
