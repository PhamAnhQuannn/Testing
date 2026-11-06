"""Inputs of check-x665-accuracy; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[1, 0, 1, 1], [1, 1, 1, 0]]},
    {"id": "s2", "args": [["cat", "dog"], ["cat", "dog"]]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        size = (x >> 8) % 9
        yt = []
        yp = []
        for _j in range(size):
            x = (x * 1103515245 + 12345) % 2147483648
            yt.append((x >> 8) % 3)
            x = (x * 1103515245 + 12345) % 2147483648
            yp.append((x >> 8) % 3)
        out.append([yt, yp])
    return out


HIDDEN = [
    {"id": "h01", "args": [[], []], "tags": ["edge"]},
    {"id": "h02", "args": [[1, 0, 1], [1, 0, 1]], "tags": ["all-correct"]},
    {"id": "h03", "args": [[1, 0, 1], [0, 1, 0]], "tags": ["all-wrong"]},
    {"id": "h04", "args": [[1], [1]], "tags": ["edge"]},
    {"id": "h05", "args": [[1], [0]], "tags": ["edge"]},
    {"id": "h06", "args": [[1, 0, 1, 1], [1, 1, 1, 0]], "tags": []},
    {"id": "h07", "args": [["a", "b", "c"], ["a", "c", "c"]], "tags": ["str"]},
    {"id": "h08", "args": [[1, 0, 0, 1, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1]], "tags": []},
]
for _i, _a in enumerate(_lcg(31, 8)):
    HIDDEN.append({"id": f"h{9 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
