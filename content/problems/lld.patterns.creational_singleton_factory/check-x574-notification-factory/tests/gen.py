"""Inputs of check-x574-notification-factory; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["email", "hi"]},
    {"id": "s2", "args": ["bogus", "x"]},
]

KINDS = ["email", "sms", "push", "fax", "Email"]
WORDS = ["hello", "code", "a b", "42", "ok!", ""]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        kind = KINDS[(x >> 8) % len(KINDS)]
        x = (x * 1103515245 + 12345) % 2147483648
        word = WORDS[(x >> 8) % len(WORDS)]
        out.append([kind, f"{word}{(x >> 12) % 100}"])
    return out


HIDDEN = [
    {"id": "h01", "args": ["email", "hello"], "tags": ["email"]},
    {"id": "h02", "args": ["sms", "code 42"], "tags": ["sms"]},
    {"id": "h03", "args": ["push", "ok!"], "tags": ["push"]},
    {"id": "h04", "args": ["fax", "msg"], "tags": ["unknown"]},
    {"id": "h05", "args": ["email", ""], "tags": ["edge"]},
    {"id": "h06", "args": ["", ""], "tags": ["edge"]},
    {"id": "h07", "args": ["EMAIL", "case"], "tags": ["unknown"]},
]
for _i, (_k, _t) in enumerate(_lcg(3, 8)):
    HIDDEN.append({"id": f"h{8 + _i:02d}", "args": [_k, _t], "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
