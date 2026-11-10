"""Inputs of check-x877-final-cwd; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["/home", ["cd projects", "cd ..", "cd /etc", "cd .."]]},
    {"id": "s2", "args": ["/a/b", ["cd c", "ls", "cd .."]]},
]

HIDDEN = [
    {"id": "h01", "args": ["/home/user", []], "tags": ["edge", "empty"]},
    {"id": "h02", "args": ["/home/user", ["cd"]], "tags": ["bare-cd"]},
    {"id": "h03", "args": ["/", ["cd .."]], "tags": ["up-at-root"]},
    {"id": "h04", "args": ["/x", ["cd .."]], "tags": ["up-to-root"]},
    {"id": "h05", "args": ["/home", ["cd /var/log", "cd nginx"]], "tags": ["absolute"]},
    {"id": "h06", "args": ["/a", ["ls", "echo hi", "pwd", "mkdir d"]], "tags": ["ignored"]},
    {"id": "h07", "args": ["/", ["cd usr", "cd local"]], "tags": ["relative"]},
    {"id": "h08", "args": ["/a", ["cd b/c/d"]], "tags": ["multi-segment"]},
    {"id": "h09", "args": ["/a/b/c", ["cd ../.."]], "tags": ["multi-up"]},
    {"id": "h10", "args": ["/a", ["cd ../../.."]], "tags": ["overshoot-root"]},
    {"id": "h11", "args": ["/a/b", ["cd ."]], "tags": ["dot"]},
    {"id": "h12", "args": ["/a/b", ["cd ./c/../d"]], "tags": ["mixed"]},
    {"id": "h13", "args": ["/a/b", ["cd /"]], "tags": ["absolute-root"]},
    {"id": "h14", "args": ["/a/b", ["cd /x/", "cd y/"]], "tags": ["trailing-slash"]},
    {"id": "h15", "args": ["/a/b/c/d/e", ["cd ..", "cd ..", "cd f", "cd"]], "tags": ["deep"]},
    {"id": "h16", "args": ["/", ["cd", "cd .", "cd .."]], "tags": ["root-noops"]},
]

_CMDS = [
    "cd",
    "cd ..",
    "cd .",
    "cd a",
    "cd b/c",
    "cd ../x",
    "cd /m/n",
    "cd /",
    "ls",
    "echo hi",
    "pwd",
]
_START = ["/", "/a", "/a/b", "/home/user"]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        start = _START[(x >> 8) % 4]
        x = _next(x)
        m = (x >> 8) % 10
        cmds = []
        for _i in range(m):
            x = _next(x)
            cmds.append(_CMDS[(x >> 8) % len(_CMDS)])
        out.append([start, cmds])
    return out


for _i, _a in enumerate(_lcg(877, 10)):
    HIDDEN.append({"id": f"h{17 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
