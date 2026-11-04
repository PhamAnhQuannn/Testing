"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [[1, 2, 3], [["add"], ["mul"]]]},
    {"id": "s2", "args": [[-3, -1, 0, 4], [["drop_below"]]]},
    {"id": "s3", "args": [[2, 5, 9], [["pow", 3], ["clip"]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[], [["add"]]], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 2, 3], []], "tags": []},
    {"id": "h03", "args": [[1, 2, 3], [["add"], ["mul"]]], "tags": []},
    {"id": "h04", "args": [[1, 2, 3], [["add", 5], ["mul", 3]]], "tags": []},
    {"id": "h05", "args": [[-3, -1, 0, 4], [["drop_below"]]], "tags": []},
    {"id": "h06", "args": [[-3, -1, 0, 4], [["drop_below", -1], ["pow"]]], "tags": []},
    {"id": "h07", "args": [[2, 5, 9], [["pow", 3], ["clip"]]], "tags": []},
    {
        "id": "h08",
        "args": [[2, 5, 9], [["clip", 6], ["add", -4], ["drop_below", 2], ["mul"]]],
        "tags": [],
    },
    {
        "id": "h09",
        "args": [[-5, 7, 3], [["add", 10], ["pow", 2], ["clip", 100], ["drop_below", 50]]],
        "tags": [],
    },
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
