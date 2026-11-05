"""Inputs of check-x549-shopping-cart.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "ops": ["ShoppingCart", "add", "add", "total", "remove", "total"],
    "args": [[], ["pen", 3, 2], ["book", 10, 1], [], ["pen"], []],
}

HIDDEN = [
    {"id": "h01", "ops": ["ShoppingCart", "total"], "args": [[], []], "tags": ["edge"]},
    {
        "id": "h02",
        "ops": ["ShoppingCart", "remove", "total"],
        "args": [[], ["ghost"], []],
        "tags": ["edge"],
    },
    {
        "id": "h03",
        "ops": ["ShoppingCart", "add", "add", "add", "total"],
        "args": [[], ["pen", 3, 2], ["pen", 3, 4], ["cup", 5, 1], []],
        "tags": [],
    },
    {
        "id": "h04",
        "ops": ["ShoppingCart", "add", "remove", "total", "add", "total"],
        "args": [[], ["a", 7, 3], ["a"], [], ["a", 7, 1], []],
        "tags": [],
    },
    {
        "id": "h05",
        "ops": ["ShoppingCart", "add", "add", "remove", "remove", "total"],
        "args": [[], ["x", 2, 2], ["y", 4, 5], ["x"], ["x"], []],
        "tags": ["edge"],
    },
    {
        "id": "h06",
        "ops": ["ShoppingCart", "add", "total", "add", "total", "remove", "total"],
        "args": [[], ["tea", 100, 0], [], ["tea", 100, 3], [], ["tea"], []],
        "tags": [],
    },
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
