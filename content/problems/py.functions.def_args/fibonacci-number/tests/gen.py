"""Hidden-test inputs for fibonacci-number; gen_hidden.py computes `expected`."""


def hidden_inputs():
    values = [0, 1, 2, 3, 4, 5, 10, 20, 29, 30]
    return [
        {
            "id": f"h{i:02d}",
            "args": [n],
            "tags": ["edge"] if n <= 1 else (["max"] if n == 30 else []),
        }
        for i, n in enumerate(values, start=1)
    ]


def small_inputs(seed, n):
    """Every n in 0..15 (the naive recursive brute stays fast)."""
    return [[k] for k in range(16)]
