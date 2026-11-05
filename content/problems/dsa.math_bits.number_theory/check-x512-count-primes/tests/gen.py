"""Inputs of check-x512-count-primes; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [10]},
    {"id": "s2", "args": [0]},
    {"id": "s3", "args": [30]},
]


def _lcg(seed, count, lo, hi):
    x = seed
    out = []
    for _ in range(count):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(lo + (x >> 8) % (hi - lo + 1))
    return out


HIDDEN = [
    {"id": "h01", "args": [0], "tags": ["edge"]},
    {"id": "h02", "args": [1], "tags": ["edge"]},
    {"id": "h03", "args": [2], "tags": ["edge"]},
    {"id": "h04", "args": [3], "tags": ["edge"]},
    {"id": "h05", "args": [4], "tags": []},
    {"id": "h06", "args": [100], "tags": []},
    {"id": "h07", "args": [97], "tags": []},
    {"id": "h08", "args": [98], "tags": []},
    {"id": "h09", "args": [10000], "tags": []},
    {"id": "h10", "args": [499979], "tags": []},
]
for _k, _v in enumerate(_lcg(7, 3, 1000, 200000)):
    HIDDEN.append({"id": f"h{11 + _k}", "args": [_v], "tags": []})
HIDDEN.append({"id": "h14", "args": [1000000], "tags": ["large"]})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
