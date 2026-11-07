"""Inputs of check-x802-index-lookup; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[10, 20, 30, 40], [30, 25, 10]]},
    {"id": "s2", "args": [[], []]},
]

HIDDEN = [
    {"id": "h01", "args": [[], [1, 2, 3]], "tags": ["edge", "empty_keys"]},
    {"id": "h02", "args": [[1, 2, 3], []], "tags": ["edge", "empty_targets"]},
    {"id": "h03", "args": [[10, 20, 30], [5, 1, -4]], "tags": ["edge", "below_min"]},
    {"id": "h04", "args": [[10, 20, 30], [31, 99]], "tags": ["edge", "above_max"]},
    {"id": "h05", "args": [[10, 20, 30, 40, 50], [10, 50]], "tags": ["edge", "first_last"]},
    {"id": "h06", "args": [[10, 20, 30, 40, 50], [25, 35]], "tags": ["absent_middle"]},
    {"id": "h07", "args": [[7], [7, 6, 8]], "tags": ["edge", "single"]},
    {"id": "h08", "args": [[-5, -2, 0, 3, 8], [-5, 0, 8, 1]], "tags": ["negatives"]},
    {"id": "h09", "args": [[2, 4, 6, 8], [8, 6, 4, 2, 8]], "tags": ["repeated_targets"]},
    {"id": "h10", "args": [[1, 2], [2, 1, 0, 3]], "tags": ["edge", "two_keys"]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        length = (x >> 8) % 12
        keys = []
        cur = (x >> 12) % 11 - 5
        for _r in range(length):
            x = (x * 1103515245 + 12345) % 2147483648
            cur += (x >> 8) % 5 + 1
            keys.append(cur)
        x = (x * 1103515245 + 12345) % 2147483648
        m = (x >> 8) % 9
        targets = []
        for _r in range(m):
            x = (x * 1103515245 + 12345) % 2147483648
            if keys and (x >> 8) % 2 == 0:
                x = (x * 1103515245 + 12345) % 2147483648
                targets.append(keys[(x >> 8) % len(keys)])
            else:
                x = (x * 1103515245 + 12345) % 2147483648
                targets.append((x >> 8) % 70 - 10)
        out.append([keys, targets])
    return out


for _i, _a in enumerate(_lcg(23, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
