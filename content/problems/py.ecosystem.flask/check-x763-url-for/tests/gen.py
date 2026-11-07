"""Inputs of check-x763-url-for; `expected` comes from solution.py via gen_hidden."""

_R = [["get_user", "/users/{id}"], ["get_post", "/users/{id}/posts/{pid}"]]

SAMPLES = [
    {"id": "s1", "args": [_R, "get_post", {"id": 7, "pid": 3}]},
    {"id": "s2", "args": [_R, "missing", {}]},
]

HIDDEN = [
    {"id": "h01", "args": [[], "any", {}], "tags": ["edge"]},
    {"id": "h02", "args": [[["home", "/"]], "home", {}], "tags": ["edge"]},
    {"id": "h03", "args": [_R, "get_user", {"id": 42}], "tags": []},
    {"id": "h04", "args": [_R, "get_post", {"id": "ann", "pid": "p9"}], "tags": ["edge"]},
    {
        "id": "h05",
        "args": [[["a", "/first/{x}"], ["a", "/second/{x}"]], "a", {"x": 1}],
        "tags": ["edge"],
    },
    {"id": "h06", "args": [[["a", "/x/{n}"], ["b", "/y"]], "b", {"n": 5}], "tags": ["edge"]},
    {"id": "h07", "args": [[["a", "/{k}/{k}"]], "a", {"k": 3}], "tags": ["edge"]},
    {
        "id": "h08",
        "args": [[["a", "/v/{a}-{b}.{c}"]], "a", {"a": 1, "b": "two", "c": 0}],
        "tags": [],
    },
    {"id": "h09", "args": [_R, "GET_USER", {"id": 1}], "tags": ["edge"]},
    {"id": "h10", "args": [_R, "get_user", {"id": 0}], "tags": ["edge"]},
]

_ENDPOINTS = ["list", "detail", "edit", "search", "tags"]
_PATTERNS = [
    "/items",
    "/items/{id}",
    "/items/{id}/edit",
    "/u/{user}/p/{pid}",
    "/s/{q}/{page}/{sort}",
]
_NAMES = ["id", "user", "pid", "q", "page", "sort"]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        n_rules = 1 + (x >> 8) % 4
        rules = []
        for _r in range(n_rules):
            x = (x * 1103515245 + 12345) % 2147483648
            ep = _ENDPOINTS[(x >> 8) % len(_ENDPOINTS)]
            x = (x * 1103515245 + 12345) % 2147483648
            pat = _PATTERNS[(x >> 8) % len(_PATTERNS)]
            rules.append([ep, pat])
        x = (x * 1103515245 + 12345) % 2147483648
        pick = (x >> 8) % (n_rules + 1)
        endpoint = "missing" if pick == n_rules else rules[pick][0]
        params = {}
        for name in _NAMES:
            x = (x * 1103515245 + 12345) % 2147483648
            v = (x >> 8) % 100
            params[name] = v if v % 2 == 0 else "s" + str(v)
        out.append([rules, endpoint, params])
    return out


for _i, _a in enumerate(_lcg(23, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
