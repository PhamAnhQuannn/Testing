"""Inputs of check-x769-run-pipeline; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["add", 2], ["mul", 3], ["clip", 0, 20]], [1, 5, -4]]},
    {"id": "s2", "args": [[], [3, 1, 2]]},
]

HIDDEN = [
    {"id": "h01", "args": [[], []], "tags": ["edge"]},
    {"id": "h02", "args": [[["add", 1]], []], "tags": ["edge"]},
    {"id": "h03", "args": [[], [5, -5, 0]], "tags": ["edge"]},
    {"id": "h04", "args": [[["add", -3]], [1, 2, 3]], "tags": ["edge"]},
    {"id": "h05", "args": [[["mul", -2]], [4, -1, 0]], "tags": ["edge"]},
    {"id": "h06", "args": [[["clip", 10, 20]], [1, 5, 9]], "tags": ["edge"]},
    {"id": "h07", "args": [[["clip", -20, -10]], [1, 5, 9]], "tags": ["edge"]},
    {"id": "h08", "args": [[["add", 2], ["mul", 3]], [1, 2, 3]], "tags": ["order"]},
    {"id": "h09", "args": [[["mul", 3], ["add", 2]], [1, 2, 3]], "tags": ["order"]},
    {"id": "h10", "args": [[["add", 5], ["clip", 0, 10]], [2, 8, -3]], "tags": ["order"]},
    {"id": "h11", "args": [[["clip", 0, 10], ["add", 5]], [2, 8, -3]], "tags": ["order"]},
    {"id": "h12", "args": [[["mul", 0], ["add", 4]], [7, -7]], "tags": ["edge"]},
    {"id": "h13", "args": [[["clip", 3, 3]], [1, 3, 9]], "tags": ["edge"]},
]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_steps = (x >> 8) % 5
        steps = []
        for _s in range(n_steps):
            x = (x * 1103515245 + 12345) % 2147483648
            kind = (x >> 8) % 3
            x = (x * 1103515245 + 12345) % 2147483648
            a = (x >> 8) % 11 - 5
            if kind == 0:
                steps.append(["add", a])
            elif kind == 1:
                steps.append(["mul", a])
            else:
                x = (x * 1103515245 + 12345) % 2147483648
                span = (x >> 8) % 8
                steps.append(["clip", a, a + span])
        x = (x * 1103515245 + 12345) % 2147483648
        n_xs = (x >> 8) % 9
        xs = []
        for _r in range(n_xs):
            x = (x * 1103515245 + 12345) % 2147483648
            xs.append((x >> 8) % 41 - 20)
        out.append([steps, xs])
    return out


for _i, _a in enumerate(_lcg(29, 12)):
    HIDDEN.append({"id": f"h{14 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
