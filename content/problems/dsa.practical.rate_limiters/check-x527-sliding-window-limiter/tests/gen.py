"""Inputs of check-x527-sliding-window-limiter; `expected` comes from solution.py via gen_hidden."""

N = "SlidingWindowLimiter"


def _case(cid, limit, window, stamps, tags=()):
    return {
        "id": cid,
        "ops": [N] + ["allow"] * len(stamps),
        "args": [[limit, window]] + [[t] for t in stamps],
        "tags": list(tags),
    }


SAMPLE = _case("s1", 2, 10, [1, 2, 3, 11, 12])

HIDDEN = [
    _case("h01", 3, 10, [5, 5, 5, 5, 5], ["edge"]),
    _case("h02", 2, 10, [0, 1, 10, 11, 12], ["edge"]),
    _case("h03", 1, 5, [0, 4, 5, 9, 10, 14, 15], ["edge"]),
    _case("h04", 2, 3, [1, 1, 1, 2, 3, 4, 4, 5, 6], []),
    _case("h05", 3, 100, [0, 10, 20, 30, 99, 100, 101, 110, 120], []),
    _case("h06", 1, 1, [0, 0, 1, 1, 2, 3, 3], []),
    _case("h07", 4, 7, list(range(0, 40, 2)), []),
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
