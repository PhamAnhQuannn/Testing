"""Inputs of check-x368-safe-get; expected comes from solution.py."""

SAMPLE = {"id": "s1", "args": [[["a", 1], ["b", 2]], ["a", "z", "b"], 0]}

HIDDEN = [
    {"id": "h01", "args": [[], ["a"], -1], "tags": ["edge"]},
    {"id": "h02", "args": [[["a", 1]], [], 0], "tags": ["edge"]},
    {"id": "h03", "args": [[["x", 10], ["y", 20]], ["y", "x"], 0], "tags": []},
    {"id": "h04", "args": [[["k", 1], ["k", 2]], ["k"], 0], "tags": []},
    {"id": "h05", "args": [[["a", 1]], ["b", "c"], "none"], "tags": []},
    {"id": "h06", "args": [[["a", 1], ["b", 2], ["c", 3]], ["c", "a", "d", "a"], None], "tags": []},
    {"id": "h07", "args": [[[1, "one"], [2, "two"]], [2, 3, 1], ""], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
