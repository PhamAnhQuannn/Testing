"""Inputs of check-x478; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["abcde", "ace"]},
    {"id": "s2", "args": ["abc", "abc"]},
    {"id": "s3", "args": ["abc", "def"]},
]


def _rand(seed, length, alphabet):
    """Seeded LCG string over `alphabet`."""
    x = seed
    out = []
    for _ in range(length):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(alphabet[(x >> 8) % len(alphabet)])
    return "".join(out)


HIDDEN = [
    {"id": "h01", "args": ["", ""], "tags": ["edge"]},
    {"id": "h02", "args": ["", "abc"], "tags": ["edge"]},
    {"id": "h03", "args": ["abc", ""], "tags": ["edge"]},
    {"id": "h04", "args": ["abc", "abc"], "tags": ["edge"]},
    {"id": "h05", "args": ["abc", "def"], "tags": ["edge"]},
    {"id": "h06", "args": ["a", "a"], "tags": ["edge"]},
    {"id": "h07", "args": ["aaaa", "aa"], "tags": []},
    {"id": "h08", "args": [_rand(1, 12, "ab"), _rand(2, 10, "ab")], "tags": []},
    {"id": "h09", "args": [_rand(3, 25, "abc"), _rand(4, 30, "abc")], "tags": []},
    {"id": "h10", "args": [_rand(5, 40, "abcd"), _rand(6, 35, "abcd")], "tags": []},
    {"id": "h11", "args": [_rand(7, 60, "ab"), _rand(8, 55, "ab")], "tags": []},
    {"id": "h12", "args": [_rand(9, 50, "abcdefgh"), _rand(10, 50, "abcdefgh")], "tags": []},
    {"id": "h13", "args": ["abcdefghij", "jihgfedcba"], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
