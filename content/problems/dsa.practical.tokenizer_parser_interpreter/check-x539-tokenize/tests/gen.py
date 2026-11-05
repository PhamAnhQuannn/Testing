"""Inputs of check-x539-tokenize; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["12+3*(4-5)"]},
    {"id": "s2", "args": ["7"]},
    {"id": "s3", "args": [" 100 / 25 - 3 "]},
]

HIDDEN = [
    {"id": "h01", "args": ["0"], "tags": ["edge"]},
    {"id": "h02", "args": ["123456"], "tags": ["edge"]},
    {"id": "h03", "args": ["((1))"], "tags": ["edge"]},
    {"id": "h04", "args": ["1+2-3*4/5"], "tags": []},
    {"id": "h05", "args": ["   8 *  ( 15 + 2 )   "], "tags": ["edge"]},
    {"id": "h06", "args": ["((2+3)*(4-1))/(5+10)"], "tags": ["edge"]},
    {"id": "h07", "args": ["10+20+30+40"], "tags": []},
    {"id": "h08", "args": ["1 2 + 3"], "tags": []},
    {"id": "h09", "args": ["(((((9)))))"], "tags": ["edge"]},
    {"id": "h10", "args": ["999999999*999999999-1"], "tags": []},
    {"id": "h11", "args": ["4/2/1"], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
