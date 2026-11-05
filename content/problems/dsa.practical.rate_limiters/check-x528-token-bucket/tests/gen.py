"""Inputs of check-x528-token-bucket; `expected` comes from solution.py via gen_hidden."""

N = "TokenBucket"


def _case(cid, cap, rate, calls, tags=()):
    return {
        "id": cid,
        "ops": [N] + ["allow"] * len(calls),
        "args": [[cap, rate]] + [[t, c] for t, c in calls],
        "tags": list(tags),
    }


SAMPLE = _case("s1", 5, 1, [(0, 3), (0, 3), (1, 3), (3, 3), (10, 6)])

HIDDEN = [
    _case("h01", 5, 1, [(0, 5), (0, 1), (1, 1), (1, 1), (3, 2), (3, 1)], ["edge"]),
    _case("h02", 3, 2, [(0, 3), (0, 1), (1, 2), (1, 1), (100, 3), (100, 1)], ["edge"]),
    _case("h03", 10, 0, [(0, 4), (5, 4), (9, 4), (100, 2), (200, 1)], ["edge"]),
    _case("h04", 4, 1, [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (4, 4), (8, 4)], []),
    _case("h05", 6, 3, [(0, 6), (1, 2), (1, 2), (2, 5), (2, 3), (3, 3)], []),
    _case("h06", 2, 1, [(0, 3), (0, 2), (1, 1), (2, 1), (3, 2)], []),
    _case("h07", 20, 5, [(i, 7) for i in range(0, 15)], []),
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
