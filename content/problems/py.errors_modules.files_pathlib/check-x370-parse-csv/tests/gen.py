"""Inputs of check-x370-parse-csv: generated, do not edit by hand.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLE = {"id": "s1", "args": ["name,age\nAn,20\nBinh,31\n"]}

HIDDEN = [
    {"id": "h01", "args": [""], "tags": ["edge"]},
    {"id": "h02", "args": ["name,age\n"], "tags": ["edge"]},
    {"id": "h03", "args": ["a,b\n1,2"], "tags": []},
    {"id": "h04", "args": ['id,city\n1,"Ha Noi, VN"\n2,Hue\n'], "tags": []},
    {"id": "h05", "args": ["x\n1\n\n2\n"], "tags": ["edge"]},
    {"id": "h06", "args": ['k,v\n"say ""hi""",9\n'], "tags": []},
    {"id": "h07", "args": ["a,b,c\n1,2,3\n4,5,6\n7,8,9\n"], "tags": []},
]


def sample_inputs():
    return [SAMPLE]


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
