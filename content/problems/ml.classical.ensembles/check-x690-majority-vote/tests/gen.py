"""Inputs of check-x690-majority-vote; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[0, 1, 1], [0, 0, 1], [1, 0, 1]]]},
    {"id": "s2", "args": [[[1, 2], [2, 1]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[[3, 1, 4, 1, 5]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[2, 2, 2], [2, 2, 2], [2, 2, 2]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[5], [3]]], "tags": ["edge"]},
    {"id": "h04", "args": [[[7], [7], [7], [7]]], "tags": ["edge"]},
    {"id": "h05", "args": [[[1, 0], [0, 1], [1, 1], [0, 0]]], "tags": ["edge"]},
    {"id": "h06", "args": [[[0, 1, 2], [1, 1, 2], [2, 1, 0]]], "tags": []},
    {"id": "h07", "args": [[[4, 4, 9], [9, 4, 9], [4, 9, 9], [9, 9, 4], [4, 4, 4]]], "tags": []},
    {"id": "h08", "args": [[[-1, 0], [-1, 1], [0, 1]]], "tags": []},
    {"id": "h09", "args": [[[0, 0, 0, 1, 1, 1], [1, 1, 1, 0, 0, 0]]], "tags": ["edge"]},
    {"id": "h10", "args": [[[3, 2, 1], [3, 2, 1], [1, 2, 3]]], "tags": []},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_models = 1 + (x >> 8) % 7
        x = (x * 1103515245 + 12345) % 2147483648
        n_samples = 1 + (x >> 8) % 8
        preds = []
        for _m in range(n_models):
            row = []
            for _j in range(n_samples):
                x = (x * 1103515245 + 12345) % 2147483648
                row.append((x >> 8) % 4)
            preds.append(row)
        out.append([preds])
    return out


for _i, _a in enumerate(_lcg(11, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
