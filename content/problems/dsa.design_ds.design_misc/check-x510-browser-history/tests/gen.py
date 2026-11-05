"""Inputs of check-x510: hand-authored class_ops cases.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["BrowserHistory", "visit", "visit", "back", "forward", "visit", "forward", "back"],
    "args": [["a.com"], ["b.com"], ["c.com"], [1], [1], ["d.com"], [3], [2]],
}


def _case(cid, home, spec, tags):
    """spec: space-separated 'v:url' / 'b:n' / 'f:n' tokens."""
    names = {"v": "visit", "b": "back", "f": "forward"}
    calls = []
    for tok in spec.split():
        kind, val = tok.split(":")
        calls.append((names[kind], val if kind == "v" else int(val)))
    return {
        "id": cid,
        "ops": ["BrowserHistory"] + [c[0] for c in calls],
        "args": [[home]] + [[c[1]] for c in calls],
        "tags": tags,
    }


HIDDEN = [
    _case("h01", "h", "b:5 f:5", ["edge"]),
    _case("h02", "h", "v:a v:b b:1 v:c f:1", ["edge"]),
    _case("h03", "h", "v:a v:b v:c b:2 b:9 f:1 f:100", []),
    _case("h04", "h", "v:a b:1 v:b b:1 f:1", []),
    _case("h05", "x", "v:y v:z b:2 v:w b:1 f:1 f:1", []),
    _case("h06", "p", "v:q v:r v:s b:3 f:2 b:1 v:t f:1 b:100", []),
    _case("h07", "h", "v:a v:a b:1 f:1 f:1", []),
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
