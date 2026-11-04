"""Inputs of check-x376-hello-chain; `expected` is recorded from solution.py by gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["BC"]},
    {"id": "s2", "args": ["CB"]},
    {"id": "s3", "args": ["B"]},
]

HIDDEN = [
    {"id": "h01", "args": [""], "tags": ["edge"]},
    {"id": "h02", "args": ["B"], "tags": []},
    {"id": "h03", "args": ["C"], "tags": []},
    {"id": "h04", "args": ["BC"], "tags": []},
    {"id": "h05", "args": ["CB"], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
