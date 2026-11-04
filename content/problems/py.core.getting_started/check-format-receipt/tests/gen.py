"""Test inputs; expected recorded by tools/gen_hidden.py."""

SAMPLES = [
    {"id": "s1", "args": [["pen,2,150", "book,1,1250"]]},
    {"id": "s2", "args": [[]]},
    {"id": "s3", "args": [["tea,3,5"]]},
]

HIDDEN = [
    {"id": "h01", "args": [["a,1,1"]], "tags": ["edge"]},
    {"id": "h02", "args": [["x,0,500"]], "tags": []},
    {"id": "h03", "args": [["gum,10,99", "mug,1,100000"]], "tags": []},
    {"id": "h04", "args": [["pen,2,150", "book,1,1250", "bag,3,0"]], "tags": []},
    {"id": "h05", "args": [["milk,1,100"]], "tags": []},
    {"id": "h06", "args": [["a,1,5", "b,2,5", "c,3,5"]], "tags": []},
    {"id": "h07", "args": [["cake,1,999", "cake,1,1"]], "tags": []},
    {"id": "h08", "args": [["z,7,1428"]], "tags": []},
    {"id": "h09", "args": [[]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
