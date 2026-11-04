"""Inputs of check-x416-type-format.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": ["int"]},
    {"id": "s2", "args": ["list[int]"]},
    {"id": "s3", "args": ["Optional[str]"]},
]

HIDDEN = [
    {"id": "h01", "args": ["str"], "tags": ["edge"]},
    {"id": "h02", "args": ["dict[str, int]"], "tags": []},
    {"id": "h03", "args": ["tuple[int, ...]"], "tags": []},
    {"id": "h04", "args": ["int | None"], "tags": []},
    {"id": "h05", "args": ["Union[int, str]"], "tags": []},
    {"id": "h06", "args": ["dict[str, list[int]]"], "tags": []},
    {"id": "h07", "args": ["set[str]"], "tags": []},
    {"id": "h08", "args": ["Optional[list[str]]"], "tags": []},
    {"id": "h09", "args": ["list[dict[str, tuple[int, float]]]"], "tags": []},
    {"id": "h10", "args": ["Callable[[int, str], bool]"], "tags": []},
    {"id": "h11", "args": ["list[Any]"], "tags": []},
    {"id": "h12", "args": ["list[int | str]"], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
