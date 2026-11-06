"""Inputs of check-x631-dispatch; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["add", 3, 4]},
    {"id": "s2", "args": ["max", 2, 9]},
]

OPS = ["add", "sub", "mul", "max", "min", "pow", "div", ""]

HIDDEN = [
    {"id": "h01", "args": ["add", 3, 4], "tags": []},
    {"id": "h02", "args": ["sub", 3, 10], "tags": []},
    {"id": "h03", "args": ["mul", -6, 7], "tags": []},
    {"id": "h04", "args": ["max", -5, -2], "tags": []},
    {"id": "h05", "args": ["min", -5, -2], "tags": []},
    {"id": "h06", "args": ["max", 4, 4], "tags": ["edge"]},
    {"id": "h07", "args": ["min", 4, 4], "tags": ["edge"]},
    {"id": "h08", "args": ["pow", 2, 3], "tags": ["edge"]},
    {"id": "h09", "args": ["", 5, 5], "tags": ["edge"]},
    {"id": "h10", "args": ["mul", 0, 123456], "tags": ["edge"]},
    {"id": "h11", "args": ["ADD", 1, 2], "tags": ["edge"]},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    x = seed
    out = []
    for i in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        op = OPS[(x >> 8) % len(OPS)]
        x = (x * 1103515245 + 12345) % 2147483648
        a = (x >> 8) % 41 - 20
        x = (x * 1103515245 + 12345) % 2147483648
        b = (x >> 8) % 41 - 20
        out.append({"id": f"r{i}", "args": [op, a, b]})
    return out
