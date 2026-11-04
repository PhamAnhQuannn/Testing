"""Inputs of check-x415-hint-names.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": ["def f(a: int, b: str) -> bool:\n    return True\n", "f"]},
    {"id": "s2", "args": ["def g(x: float) -> None:\n    pass\n", "g"]},
    {"id": "s3", "args": ["def h():\n    pass\n", "h"]},
]

HIDDEN = [
    {"id": "h01", "args": ["def f():\n    return 1\n", "f"], "tags": ["edge"]},
    {"id": "h02", "args": ["def f(a: int) -> int:\n    return a\n", "f"], "tags": []},
    {"id": "h03", "args": ["def f(a, b: str, c) -> str:\n    return b\n", "f"], "tags": []},
    {
        "id": "h04",
        "args": ["def f(x: list, y: dict = None) -> set:\n    return set()\n", "f"],
        "tags": [],
    },
    {"id": "h05", "args": ["def f(x: 'int') -> 'str':\n    return ''\n", "f"], "tags": []},
    {
        "id": "h06",
        "args": ["def a(x: int):\n    pass\n\n\ndef b(y: str) -> float:\n    return 1.0\n", "b"],
        "tags": [],
    },
    {
        "id": "h07",
        "args": ["def f(*, z: bytes, a: bool = True) -> tuple:\n    return ()\n", "f"],
        "tags": [],
    },
    {"id": "h08", "args": ["def f(n: int) -> None:\n    return None\n", "f"], "tags": []},
    {"id": "h09", "args": ["def zed(b: str, a: int):\n    pass\n", "zed"], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
