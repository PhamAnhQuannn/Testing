"""Inputs of check-x374: days between two dates via datetime.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": ["2026-01-01", "2026-03-01"]}

HIDDEN = [
    {"id": "h01", "args": ["2026-05-05", "2026-05-05"], "tags": ["edge"]},
    {"id": "h02", "args": ["2026-01-01", "2026-01-02"], "tags": []},
    {"id": "h03", "args": ["2026-03-01", "2026-01-01"], "tags": []},
    {"id": "h04", "args": ["2024-02-28", "2024-03-01"], "tags": ["leap"]},
    {"id": "h05", "args": ["2025-02-28", "2025-03-01"], "tags": []},
    {"id": "h06", "args": ["2025-12-31", "2026-01-01"], "tags": []},
    {"id": "h07", "args": ["2000-01-01", "2026-11-04"], "tags": []},
    {"id": "h08", "args": ["2026-11-04", "2020-02-29"], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
