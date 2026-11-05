"""Inputs of check-x540-eval-expr; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["12+3*(4-5)"]},
    {"id": "s2", "args": ["42"]},
    {"id": "s3", "args": ["2+3*4-6/2"]},
]

HIDDEN = [
    {"id": "h01", "args": ["0"], "tags": ["edge"]},
    {"id": "h02", "args": ["  17  "], "tags": ["edge"]},
    {"id": "h03", "args": ["2+3*4"], "tags": ["edge"]},
    {"id": "h04", "args": ["(2+3)*4"], "tags": []},
    {"id": "h05", "args": ["((((5))))"], "tags": ["edge"]},
    {"id": "h06", "args": ["((1+2)*(3+4)-(5-6))/(7-5)"], "tags": ["edge"]},
    {"id": "h07", "args": ["10-3-2"], "tags": []},
    {"id": "h08", "args": ["100/10/5"], "tags": []},
    {"id": "h09", "args": ["7/2"], "tags": []},
    {"id": "h10", "args": ["1-8/3"], "tags": []},
    {"id": "h11", "args": ["(1-10)/2"], "tags": ["edge"]},
    {"id": "h12", "args": ["2*(3+(4*(5-(6/2))))"], "tags": ["edge"]},
    {"id": "h13", "args": ["123*456+789/3-1000"], "tags": []},
    {"id": "h14", "args": ["1+2+3+4+5+6+7+8+9+10"], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
