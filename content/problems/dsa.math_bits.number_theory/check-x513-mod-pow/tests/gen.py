"""Inputs of check-x513-mod-pow; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [2, 10, 1000]},
    {"id": "s2", "args": [5, 0, 7]},
    {"id": "s3", "args": [3, 200, 13]},
]

MOD = 10**9 + 7


def _lcg(seed, count):
    x = seed
    out = []
    for _ in range(count):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(x)
    return out


HIDDEN = [
    {"id": "h01", "args": [7, 0, 5], "tags": ["edge"]},
    {"id": "h02", "args": [7, 0, 1], "tags": ["edge"]},
    {"id": "h03", "args": [9, 5, 1], "tags": ["edge"]},
    {"id": "h04", "args": [0, 0, 9], "tags": ["edge"]},
    {"id": "h05", "args": [0, 5, 9], "tags": ["edge"]},
    {"id": "h06", "args": [1, 10**18, MOD], "tags": []},
    {"id": "h07", "args": [2, 1, 1000], "tags": []},
    {"id": "h08", "args": [10, 18, 10**9], "tags": []},
    {"id": "h09", "args": [2, 10**18, MOD], "tags": ["large"]},
    {"id": "h10", "args": [10**9, 10**18, MOD], "tags": ["large"]},
]
_r = _lcg(11, 12)
for _k in range(4):
    HIDDEN.append(
        {
            "id": f"h{11 + _k}",
            "args": [
                _r[3 * _k] % (10**9 + 1),
                _r[3 * _k + 1] * 400_000_000,
                _r[3 * _k + 2] % MOD + 1,
            ],
            "tags": [],
        }
    )


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
