"""Inputs of check-x473-decode-ways; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["226"]},
    {"id": "s2", "args": ["12"]},
    {"id": "s3", "args": ["06"]},
]


def _lcg_digits(seed, n, alphabet):
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(alphabet[(x >> 8) % len(alphabet)])
    return "".join(out)


HIDDEN = [
    {"id": "h01", "args": ["0"], "tags": ["edge"]},
    {"id": "h02", "args": ["06"], "tags": ["edge"]},
    {"id": "h03", "args": ["10"], "tags": ["edge"]},
    {"id": "h04", "args": ["27"], "tags": ["edge"]},
    {"id": "h05", "args": ["100"], "tags": ["edge"]},
    {"id": "h06", "args": ["1"], "tags": ["edge"]},
    {"id": "h07", "args": ["2101"], "tags": []},
    {"id": "h08", "args": ["1" * 45], "tags": []},
    {"id": "h09", "args": [_lcg_digits(1, 12, "0123456789")], "tags": []},
    {"id": "h10", "args": ["1" + _lcg_digits(2, 30, "1226")], "tags": []},
    {"id": "h11", "args": ["2" + _lcg_digits(3, 40, "0126")], "tags": []},
    {"id": "h12", "args": ["1" + _lcg_digits(4, 44, "12036")], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
