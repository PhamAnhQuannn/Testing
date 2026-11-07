"""Inputs of check-x739-parse-requirements; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {
        "id": "s1",
        "args": [
            [
                "requests==2.31.0",
                "# a comment",
                "",
                "flask>=2.0",
                "uvicorn[standard]==0.23.0",
                "numpy",
            ]
        ],
    },
    {"id": "s2", "args": [["# only a comment", "", "   "]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge"]},
    {"id": "h02", "args": [["# a", "   ", "", "  # b"]], "tags": ["edge"]},
    {"id": "h03", "args": [["numpy", "pandas", "  scipy  "]], "tags": ["edge"]},
    {
        "id": "h04",
        "args": [["uvicorn[standard]==0.23.0", "pkg[a,b]>=1.0", "x[y]"]],
        "tags": ["edge"],
    },
    {"id": "h05", "args": [["a==1", "b>=2", "c<=3", "d~=4.1", "e!=5", "f>6", "g<7"]], "tags": []},
    {"id": "h06", "args": [["requests==2.31.0  # pinned", "flask>=2.0 # min"]], "tags": ["edge"]},
    {"id": "h07", "args": [["  django  >=  4.2  ", "\tpytest == 7.4.0"]], "tags": ["edge"]},
    {"id": "h08", "args": [["black>=23.1.0", "ruff>0.1", "mypy<2"]], "tags": []},
    {"id": "h09", "args": [["lib~=1.4.2", "tool!=0.9", "numpy"]], "tags": []},
    {"id": "h10", "args": [["# header", "a==1.0", "", "b[x]>=2  # c", "c"]], "tags": []},
]

_NAMES = ["requests", "flask", "numpy", "pandas", "django", "pytest", "uvicorn", "black"]
_OPS = ["==", ">=", "<=", "~=", "!=", ">", "<", ""]
_VERS = ["1.0", "2.31.0", "0.9", "3.1.4", "1.10.0", "4.2", "0.0.1"]
_EXTRAS = ["", "", "[extra]", "[a,b]"]
_PAD = ["", " ", "  "]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_lines = (x >> 8) % 8
        lines = []
        for _l in range(n_lines):
            x = (x * 1103515245 + 12345) % 2147483648
            kind = (x >> 8) % 6
            if kind == 0:
                x = (x * 1103515245 + 12345) % 2147483648
                lines.append("# note " + _NAMES[(x >> 8) % len(_NAMES)])
                continue
            if kind == 1:
                x = (x * 1103515245 + 12345) % 2147483648
                lines.append(_PAD[(x >> 8) % len(_PAD)])
                continue
            x = (x * 1103515245 + 12345) % 2147483648
            name = _NAMES[(x >> 8) % len(_NAMES)]
            x = (x * 1103515245 + 12345) % 2147483648
            extra = _EXTRAS[(x >> 8) % len(_EXTRAS)]
            x = (x * 1103515245 + 12345) % 2147483648
            op = _OPS[(x >> 8) % len(_OPS)]
            x = (x * 1103515245 + 12345) % 2147483648
            ver = _VERS[(x >> 8) % len(_VERS)]
            x = (x * 1103515245 + 12345) % 2147483648
            pad = _PAD[(x >> 8) % len(_PAD)]
            line = name + extra + (pad + op + pad + ver if op else "")
            x = (x * 1103515245 + 12345) % 2147483648
            if (x >> 8) % 4 == 0:
                line = line + "  # inline"
            lines.append(pad + line)
        out.append([lines])
    return out


for _i, _a in enumerate(_lcg(13, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
