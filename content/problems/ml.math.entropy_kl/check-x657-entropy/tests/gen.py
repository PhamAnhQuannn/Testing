"""Inputs of check-x657-entropy; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[0.5, 0.5]]},
    {"id": "s2", "args": [[0.25, 0.25, 0.25, 0.25]]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        size = 2 + (x >> 8) % 5
        weights = []
        for _j in range(size):
            x = (x * 1103515245 + 12345) % 2147483648
            w = (x >> 8) % 10
            weights.append(w)
        if sum(weights) == 0:
            weights[0] = 1
        total = sum(weights)
        out.append([[round(w / total, 6) for w in weights]])
    return out


HIDDEN = [
    {"id": "h01", "args": [[1.0]], "tags": ["edge"]},
    {"id": "h02", "args": [[0.5, 0.5, 0.0]], "tags": ["edge", "zero_prob"]},
    {"id": "h03", "args": [[0.0, 1.0]], "tags": ["edge", "zero_prob"]},
    {"id": "h04", "args": [[0.9, 0.1]], "tags": []},
    {"id": "h05", "args": [[0.5, 0.25, 0.125, 0.125]], "tags": []},
    {"id": "h06", "args": [[0.125] * 8], "tags": []},
    {"id": "h07", "args": [[0.2, 0.2, 0.2, 0.2, 0.2]], "tags": []},
    {"id": "h08", "args": [[0.7, 0.2, 0.1]], "tags": []},
    {"id": "h09", "args": [[0.0, 0.3, 0.0, 0.7]], "tags": ["zero_prob"]},
]
for _i, _a in enumerate(_lcg(11, 8)):
    HIDDEN.append({"id": f"h{10 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
