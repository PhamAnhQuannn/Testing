"""Inputs of check-x509: hand-authored class_ops cases.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["Logger"] + ["should_print_message"] * 4,
    "args": [[], [1, "foo"], [2, "bar"], [3, "foo"], [11, "foo"]],
}


def _case(cid, calls, tags):
    return {
        "id": cid,
        "ops": ["Logger"] + ["should_print_message"] * len(calls),
        "args": [[]] + [list(c) for c in calls],
        "tags": tags,
    }


HIDDEN = [
    _case("h01", [(0, "a")], ["edge"]),
    _case("h02", [(1, "a"), (10, "a"), (11, "a"), (12, "a")], ["edge"]),
    _case("h03", [(5, "x"), (5, "x"), (5, "y"), (14, "x"), (15, "x")], []),
    _case("h04", [(1, "a"), (2, "a"), (11, "a"), (12, "a"), (21, "a")], []),
    _case("h05", [(0, "a"), (0, "b"), (9, "a"), (10, "b"), (10, "a"), (19, "b")], []),
    _case("h06", [(100, "m"), (105, "m"), (109, "m"), (110, "m"), (119, "m"), (120, "m")], []),
    _case("h07", [(1000000000, "z"), (1000000000, "z")], ["edge"]),
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
