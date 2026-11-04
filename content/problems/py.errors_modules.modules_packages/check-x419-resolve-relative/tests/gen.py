"""Inputs of check-x419-resolve-relative.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": ["app.sub", 2, "utils"]},
    {"id": "s2", "args": ["app.sub", 1, "utils"]},
    {"id": "s3", "args": ["app", 0, "os.path"]},
]

HIDDEN = [
    {"id": "h01", "args": ["app", 1, ""], "tags": ["edge"]},
    {"id": "h02", "args": ["app", 2, "x"], "tags": ["edge"]},
    {"id": "h03", "args": ["app.sub", 2, ""], "tags": []},
    {"id": "h04", "args": ["a.b.c", 3, "d"], "tags": []},
    {"id": "h05", "args": ["a.b.c", 4, "d"], "tags": ["edge"]},
    {"id": "h06", "args": ["a.b.c", 1, "d.e"], "tags": []},
    {"id": "h07", "args": ["pkg", 0, "json"], "tags": []},
    {"id": "h08", "args": ["a.b", 2, ""], "tags": []},
    {"id": "h09", "args": ["a.b", 3, "z"], "tags": ["edge"]},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
