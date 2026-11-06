"""Inputs of check-x669-reg-loss; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [0.5, [1, -2], 0.1, "l2"]},
    {"id": "s2", "args": [0.5, [1, -2], 0.1, "l1"]},
]

KINDS = ["l2", "l1", "none", "l2", "l1"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        k = (x >> 8) % 5
        ws = []
        for _j in range(k):
            x = (x * 1103515245 + 12345) % 2147483648
            ws.append((x >> 8) % 13 - 6)
        x = (x * 1103515245 + 12345) % 2147483648
        base = ((x >> 8) % 41) / 10
        x = (x * 1103515245 + 12345) % 2147483648
        lam = ((x >> 8) % 6) / 10
        x = (x * 1103515245 + 12345) % 2147483648
        kind = KINDS[(x >> 8) % 5]
        out.append([base, ws, lam, kind])
    return out


HIDDEN = [
    {"id": "h01", "args": [0.5, [1, -2], 0.1, "none"], "tags": ["edge"]},
    {"id": "h02", "args": [0.5, [1, -2], 0.1, "ridge"], "tags": ["edge"]},
    {"id": "h03", "args": [1.25, [], 0.5, "l2"], "tags": ["edge"]},
    {"id": "h04", "args": [1.25, [], 0.5, "l1"], "tags": ["edge"]},
    {"id": "h05", "args": [0.3, [3, -3, 0.5], 0.0, "l2"], "tags": ["edge"]},
    {"id": "h06", "args": [0.3, [3, -3, 0.5], 0.2, "l2"], "tags": []},
    {"id": "h07", "args": [0.3, [3, -3, 0.5], 0.2, "l1"], "tags": []},
    {"id": "h08", "args": [2.0, [0.25, -0.75], 1.0, "l2"], "tags": []},
    {"id": "h09", "args": [0.0, [0, 0, 0], 3.0, "l1"], "tags": ["edge"]},
]
for _i, _a in enumerate(_lcg(5, 8)):
    HIDDEN.append({"id": f"h{10 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
