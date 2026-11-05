"""Inputs of check-x542-price-engine; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [1000, ["percent 10", "fixed 50"]]},
    {"id": "s2", "args": [500, ["fixed 200", "percent 50"]]},
    {"id": "s3", "args": [99, ["percent 33"]]},
]


def _rules(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        if (x >> 8) % 2:
            out.append(f"percent {(x >> 12) % 101}")
        else:
            out.append(f"fixed {(x >> 12) % 400}")
    return out


HIDDEN = [
    {"id": "h01", "args": [1000, []], "tags": ["edge"]},
    {"id": "h02", "args": [0, ["percent 10", "fixed 5"]], "tags": ["edge"]},
    {"id": "h03", "args": [100, ["fixed 500"]], "tags": ["edge"]},
    {"id": "h04", "args": [100, ["fixed 500", "fixed 10"]], "tags": ["edge"]},
    {"id": "h05", "args": [100, ["percent 100"]], "tags": ["edge"]},
    {"id": "h06", "args": [999, ["percent 15", "percent 15"]], "tags": []},
    {"id": "h07", "args": [1000, ["fixed 50", "percent 10"]], "tags": []},
    {"id": "h08", "args": [7, ["percent 50"]], "tags": ["edge"]},
    {"id": "h09", "args": [123456, _rules(1, 20)], "tags": []},
    {"id": "h10", "args": [50000, _rules(2, 50)], "tags": []},
    {"id": "h11", "args": [1000000, _rules(3, 100)], "tags": []},
    {"id": "h12", "args": [250, ["percent 0", "fixed 0"]], "tags": ["edge"]},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
