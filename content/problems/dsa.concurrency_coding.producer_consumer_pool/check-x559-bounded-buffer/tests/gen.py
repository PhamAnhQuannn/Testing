"""Inputs of check-x559-bounded-buffer.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["BoundedBuffer", "put", "put", "put", "get", "size", "get", "get"],
    "args": [[2], [5], [6], [7], [], [], [], []],
}

HIDDEN = [
    {"id": "h01", "ops": ["BoundedBuffer", "get", "size"], "args": [[3], [], []], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["BoundedBuffer", "put", "put", "put", "put", "size"],
        "args": [[3], [1], [2], [3], [4], []],
        "tags": ["full"],
    },
    {
        "id": "h03",
        "ops": ["BoundedBuffer", "put", "put", "put", "get", "get", "get", "get"],
        "args": [[3], [10], [20], [30], [], [], [], []],
        "tags": ["fifo"],
    },
    {
        "id": "h04",
        "ops": ["BoundedBuffer", "put", "put", "get", "put", "size", "get"],
        "args": [[1], [7], [8], [], [9], [], []],
        "tags": ["edge", "capacity1"],
    },
    {
        "id": "h05",
        "ops": [
            "BoundedBuffer",
            "put",
            "put",
            "put",
            "get",
            "put",
            "put",
            "get",
            "get",
            "get",
            "get",
        ],
        "args": [[2], [1], [2], [3], [], [4], [5], [], [], [], []],
        "tags": ["interleave"],
    },
    {
        "id": "h06",
        "ops": ["BoundedBuffer", "put", "get", "get", "put", "size", "get", "size"],
        "args": [[2], [0], [], [], [-5], [], [], []],
        "tags": ["edge"],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    """Deterministic pseudo-random op sequences (LCG, no random module)."""
    out = []
    state = seed * 2654435761 % (2**32) or 1
    for i in range(n):
        state = (state * 1103515245 + 12345) % (2**31)
        cap = 1 + state % 3
        ops = ["BoundedBuffer"]
        args = [[cap]]
        for _ in range(8):
            state = (state * 1103515245 + 12345) % (2**31)
            r = (state >> 8) % 4
            if r <= 1:
                ops.append("put")
                args.append([(state >> 4) % 20])
            elif r == 2:
                ops.append("get")
                args.append([])
            else:
                ops.append("size")
                args.append([])
        out.append({"id": f"r{i}", "ops": ops, "args": args})
    return out
