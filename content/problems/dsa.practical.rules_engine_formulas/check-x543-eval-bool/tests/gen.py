"""Inputs of check-x543-eval-bool; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["T AND ( F OR NOT F )"]},
    {"id": "s2", "args": ["T OR F AND F"]},
    {"id": "s3", "args": ["NOT ( T AND F ) AND F"]},
]


def _expr(seed, depth):
    """Deterministic random expression (always fully valid), space-separated tokens."""
    state = [seed]

    def rnd(k):
        state[0] = (state[0] * 1103515245 + 12345) % 2147483648
        return (state[0] >> 8) % k

    def build(d):
        c = rnd(6) if d > 0 else rnd(2)
        if c < 2:
            return "TF"[c]
        if c == 2:
            return "NOT " + build(d - 1)
        if c == 3:
            return "( " + build(d - 1) + " )"
        op = "AND" if c == 4 else "OR"
        return build(d - 1) + " " + op + " " + build(d - 1)

    return build(depth)


HIDDEN = [
    {"id": "h01", "args": ["T"], "tags": ["edge"]},
    {"id": "h02", "args": ["F"], "tags": ["edge"]},
    {"id": "h03", "args": ["NOT NOT T"], "tags": ["edge"]},
    {"id": "h04", "args": ["NOT NOT NOT T"], "tags": ["edge"]},
    {"id": "h05", "args": ["( ( ( F ) ) )"], "tags": ["edge"]},
    {"id": "h06", "args": ["T OR F AND F"], "tags": ["edge"]},
    {"id": "h07", "args": ["( T OR F ) AND F"], "tags": []},
    {"id": "h08", "args": ["NOT F AND F"], "tags": ["edge"]},
    {"id": "h09", "args": ["F OR F OR T AND T AND F"], "tags": []},
    {"id": "h10", "args": ["NOT ( ( T AND F ) OR ( F OR NOT T ) )"], "tags": []},
    {"id": "h11", "args": [_expr(11, 6)], "tags": []},
    {"id": "h12", "args": [_expr(12, 6)], "tags": []},
    {"id": "h13", "args": [_expr(13, 7)], "tags": []},
    {"id": "h14", "args": [_expr(14, 7)], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
