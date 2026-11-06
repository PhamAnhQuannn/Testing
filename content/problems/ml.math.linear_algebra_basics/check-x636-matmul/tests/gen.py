"""Inputs of check-x636-matmul; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[[1, 2, 3], [4, 5, 6]], [[1, 0], [0, 1], [1, 1]]]},
    {"id": "s2", "args": [[[1, 2]], [[3, 4]]]},
]

HIDDEN = [
    {"id": "h01", "args": [[[5]], [[7]]], "tags": ["edge"]},
    {"id": "h02", "args": [[[1, 2], [3, 4]], [[1, 0], [0, 1]]], "tags": ["edge"]},
    {"id": "h03", "args": [[[1, 2], [3, 4]], [[1, 2, 3]]], "tags": ["edge"]},
    {"id": "h04", "args": [[[1, 2, 3], [4, 5, 6]], [[1, 0], [0, 1], [1, 1]]], "tags": ["rect"]},
    {"id": "h05", "args": [[[1], [2], [3]], [[4, 5, 6]]], "tags": ["rect"]},
    {"id": "h06", "args": [[[1, 2, 3]], [[4], [5], [6]]], "tags": ["rect"]},
    {"id": "h07", "args": [[[-1, 2], [3, -4]], [[-5, 6], [7, -8]]], "tags": ["neg"]},
    {"id": "h08", "args": [[[0, 0], [0, 0]], [[1, 2], [3, 4]]], "tags": ["zero"]},
    {"id": "h09", "args": [[[1, 2], [3, 4], [5, 6]], [[1, 2], [3, 4], [5, 6]]], "tags": ["edge"]},
    {"id": "h10", "args": [[[1000000, -1000000]], [[1000000], [1000000]]], "tags": ["large"]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        dims = []
        for _ in range(3):
            x = (x * 1103515245 + 12345) % 2147483648
            dims.append(1 + (x >> 8) % 4)
        m, k, p = dims
        x = (x * 1103515245 + 12345) % 2147483648
        k2 = k + 1 if (x >> 8) % 5 == 0 else k
        mats = []
        for rows, cols in ((m, k), (k2, p)):
            mat = []
            for _ in range(rows):
                row = []
                for _ in range(cols):
                    x = (x * 1103515245 + 12345) % 2147483648
                    row.append((x >> 8) % 21 - 10)
                mat.append(row)
            mats.append(mat)
        out.append(mats)
    return out


for _i, _a in enumerate(_lcg(11, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
