"""Inputs of check-x447-range-sum-update; `expected` comes from solution.py via gen_hidden."""

SAMPLE = {"id": "s1", "args": [[1, 3, 5], [["q", 0, 2], ["u", 1, 10], ["q", 0, 2], ["q", 1, 1]]]}

SAMPLES = [
    SAMPLE,
    {"id": "s2", "args": [[2, 4, 6, 8], [["u", 0, 0], ["q", 0, 3], ["u", 3, -8], ["q", 2, 3]]]},
    {"id": "s3", "args": [[5], [["q", 0, 0], ["u", 0, 9], ["q", 0, 0]]]},
]


def _lcg(seed, n, lo, hi):
    out, x = [], seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(lo + x % (hi - lo + 1))
    return out


def _ops(seed, n, m):
    r = _lcg(seed, 4 * m, 0, 10**9)
    ops = []
    for k in range(m):
        a, b, c, d = r[4 * k : 4 * k + 4]
        if a % 2 == 0:
            ops.append(["u", b % n, c % 2000001 - 1000000])
        else:
            ll, rr = b % n, c % n
            ops.append(["q", min(ll, rr), max(ll, rr)])
    return ops


_BIG = _lcg(5, 1500, -1000000, 1000000)

HIDDEN = [
    {"id": "h01", "args": [[], []], "tags": ["edge"]},
    {"id": "h02", "args": [[4], [["q", 0, 0], ["u", 0, -4], ["q", 0, 0]]], "tags": ["edge"]},
    {"id": "h03", "args": [[1, 2, 3, 4, 5], [["u", 2, 3], ["q", 0, 4]]], "tags": ["edge"]},
    {
        "id": "h04",
        "args": [[1, 2, 3, 4, 5], [["u", 0, 10], ["u", 4, 20], ["q", 0, 4], ["q", 1, 3]]],
        "tags": [],
    },
    {
        "id": "h05",
        "args": [
            [0] * 8,
            [["u", 3, 1000000000], ["u", 3, -1000000000], ["q", 0, 7], ["u", 7, 5], ["q", 3, 7]],
        ],
        "tags": [],
    },
    {
        "id": "h06",
        "args": [[7, 7, 7], [["u", 1, 7], ["u", 1, 7], ["q", 0, 2], ["q", 1, 1]]],
        "tags": [],
    },
    {
        "id": "h07",
        "args": [
            list(range(1, 17)),
            [["q", 0, 15], ["u", 7, 100], ["q", 4, 11], ["u", 0, -50], ["q", 0, 7], ["q", 8, 15]],
        ],
        "tags": [],
    },
    {"id": "h08", "args": [[3, 1, 4], [["u", 0, 9], ["u", 1, 9], ["u", 2, 9]]], "tags": []},
    {"id": "h09", "args": [_BIG, _ops(3, 1500, 800)], "tags": []},
    {
        "id": "h10",
        "args": [
            [-1000000000, 1000000000, -1000000000],
            [["q", 0, 2], ["u", 1, -1000000000], ["q", 0, 2]],
        ],
        "tags": [],
    },
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
