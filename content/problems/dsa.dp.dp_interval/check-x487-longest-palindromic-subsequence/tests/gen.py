"""Inputs for this check; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["bbbab"]},
    {"id": "s2", "args": ["cbbd"]},
    {"id": "s3", "args": ["abcde"]},
]


def _rand(seed, n, alphabet):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(alphabet[(x >> 8) % len(alphabet)])
    return "".join(out)


HIDDEN = [
    {"id": "h01", "args": ["a"], "tags": ["edge"]},
    {"id": "h02", "args": [""], "tags": ["edge"]},
    {"id": "h03", "args": ["aaaaaaaaaaaa"], "tags": ["edge"]},
    {"id": "h04", "args": ["ab"], "tags": ["edge"]},
    {"id": "h05", "args": ["abcdefghij"], "tags": []},
    {"id": "h06", "args": ["racecar"], "tags": []},
    {"id": "h07", "args": [_rand(1, 20, "ab")], "tags": []},
    {"id": "h08", "args": [_rand(2, 30, "abc")], "tags": []},
    {"id": "h09", "args": [_rand(3, 45, "abcd")], "tags": []},
    {"id": "h10", "args": [_rand(4, 60, "abcdefgh")], "tags": []},
    {"id": "h11", "args": ["ab" * 25], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
