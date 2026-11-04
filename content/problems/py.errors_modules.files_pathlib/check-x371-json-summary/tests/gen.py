"""Inputs of check-x371-json-summary: generated, do not edit by hand.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {
    "id": "s1",
    "args": ['[{"name": "pen", "price": 5, "qty": 2}, {"name": "book", "price": 20, "qty": 3}]'],
}

HIDDEN = [
    {"id": "h01", "args": ["[]"], "tags": ["edge"]},
    {"id": "h02", "args": ['[{"price": 7, "qty": 1}]'], "tags": ["edge"]},
    {"id": "h03", "args": ['[{"price": 0, "qty": 9}]'], "tags": ["edge"]},
    {"id": "h04", "args": ['[{"price": 3, "qty": 4}, {"price": 3, "qty": 4}]'], "tags": []},
    {
        "id": "h05",
        "args": [
            '[{"name":"a","price":10,"qty":10},{"name":"b","price":1,"qty":0},{"name":"c","price":2,"qty":5}]'
        ],
        "tags": [],
    },
    {"id": "h06", "args": ['[\n  {"price": 100, "qty": 2}\n]'], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
