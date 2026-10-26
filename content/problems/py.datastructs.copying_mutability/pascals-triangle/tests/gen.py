"""Hidden-test inputs for pascals-triangle; gen_hidden.py computes `expected`."""


def hidden_inputs():
    sizes = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30]
    return [
        {
            "id": f"h{i:02d}",
            "args": [n],
            "tags": ["edge"] if n <= 2 else (["max"] if n == 30 else []),
        }
        for i, n in enumerate(sizes, start=1)
    ]
