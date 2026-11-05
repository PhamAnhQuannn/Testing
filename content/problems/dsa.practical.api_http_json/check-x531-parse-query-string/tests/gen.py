"""Inputs of check-x531-parse-query-string; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["a=1&b=2&a=3"]},
    {"id": "s2", "args": ["x"]},
    {"id": "s3", "args": [""]},
]


def _random_qs(seed, n):
    keys = ["a", "b", "c", "id", "page", "q"]
    x = seed
    parts = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        key = keys[(x >> 8) % len(keys)]
        x = (x * 1103515245 + 12345) % 2147483648
        if (x >> 8) % 4 == 0:
            parts.append(key)
        else:
            parts.append(key + "=" + str((x >> 8) % 1000))
    return "&".join(parts)


HIDDEN = [
    {"id": "h01", "args": [""], "tags": ["edge"]},
    {"id": "h02", "args": ["x"], "tags": ["edge"]},
    {"id": "h03", "args": ["a=1&b=2&a=3"], "tags": ["edge"]},
    {"id": "h04", "args": ["k=&j="], "tags": ["edge"]},
    {"id": "h05", "args": ["n=a=b&m==="], "tags": ["edge"]},
    {"id": "h06", "args": ["a=1&&b=2&"], "tags": ["edge"]},
    {"id": "h07", "args": ["flag&flag=on&flag"], "tags": ["edge"]},
    {"id": "h08", "args": ["page=2&limit=10&sort=asc"], "tags": []},
    {"id": "h09", "args": [_random_qs(1, 10)], "tags": []},
    {"id": "h10", "args": [_random_qs(2, 40)], "tags": []},
    {"id": "h11", "args": [_random_qs(3, 150)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
