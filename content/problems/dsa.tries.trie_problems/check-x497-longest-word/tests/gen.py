"""Inputs of check-x497-longest-word; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [["w", "wo", "wor", "worl", "world"]]},
    {"id": "s2", "args": [["a", "banana", "app", "appl", "ap", "apply", "apple"]]},
    {
        "id": "s3",
        "args": [
            [
                *["yo", "ew", "fc", "zrc", "yodn", "fcm", "qm"],
                *["qmo", "fcmz", "z", "ewq", "yod", "ewqz", "y"],
            ]
        ],
    },
]


def _lcg(seed):
    x = seed
    while True:
        x = (x * 1103515245 + 12345) % 2147483648
        yield x >> 8


def _random_words(seed, n, alpha, maxlen):
    g = _lcg(seed)
    out = []
    for _ in range(n):
        ln = 1 + next(g) % maxlen
        out.append("".join(chr(97 + next(g) % alpha) for _ in range(ln)))
    return out


def _closed(seed, n, alpha):
    """Words grown from shorter ones, so long buildable chains and ties exist."""
    g = _lcg(seed)
    out = ["a", "b"]
    for _ in range(n):
        base = out[next(g) % len(out)]
        out.append(base + chr(97 + next(g) % alpha))
    return out[:n]


HIDDEN = [
    {"id": "h01", "args": [["abc", "bcd"]], "tags": ["edge"]},
    {"id": "h02", "args": [["a"]], "tags": ["edge"]},
    {"id": "h03", "args": [["b", "a"]], "tags": ["edge"]},
    {"id": "h04", "args": [["a", "ab", "b", "bc"]], "tags": ["edge", "tie"]},
    {"id": "h05", "args": [["ab", "abc", "abcd"]], "tags": ["edge"]},
    {"id": "h06", "args": [["a", "a", "ab", "ab"]], "tags": ["edge"]},
    {
        "id": "h07",
        "args": [
            [
                *["m", "mo", "moc", "moch", "mocha"],
                *["l", "la", "lat", "latt", "latte"],
                *["c", "ca", "cat"],
            ]
        ],
        "tags": ["tie"],
    },
    {"id": "h08", "args": [_random_words(1, 40, 3, 5)], "tags": []},
    {"id": "h09", "args": [_closed(2, 60, 3)], "tags": ["tie"]},
    {"id": "h10", "args": [_closed(3, 200, 4)], "tags": ["tie"]},
    {"id": "h11", "args": [_random_words(4, 500, 2, 10)], "tags": []},
    {"id": "h12", "args": [["a" * k for k in range(1, 31)]], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
