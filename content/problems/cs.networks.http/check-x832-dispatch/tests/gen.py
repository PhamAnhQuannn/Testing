"""Inputs of check-x832-dispatch; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [[["GET", "/u", "h1"], ["POST", "/u", "h2"]], "POST", "/u"]},
    {"id": "s2", "args": [[["GET", "/u", "h1"]], "GET", "/x"]},
]

HIDDEN = [
    {"id": "h01", "args": [[], "GET", "/"], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [[["GET", "/", "home"]], "GET", "/"], "tags": ["edge", "single-hit"]},
    {"id": "h03", "args": [[["GET", "/", "home"]], "POST", "/"], "tags": ["method-mismatch"]},
    {"id": "h04", "args": [[["GET", "/a", "h1"]], "GET", "/b"], "tags": ["path-mismatch"]},
    {
        "id": "h05",
        "args": [[["GET", "/u", "h1"], ["GET", "/u", "h2"]], "GET", "/u"],
        "tags": ["first-of-duplicates"],
    },
    {
        "id": "h06",
        "args": [
            [["GET", "/users", "list"], ["POST", "/users", "create"], ["DELETE", "/users", "rm"]],
            "DELETE",
            "/users",
        ],
        "tags": ["same-path-many-methods"],
    },
    {
        "id": "h07",
        "args": [[["GET", "/a", "h1"], ["GET", "/b", "h2"], ["GET", "/c", "h3"]], "GET", "/c"],
        "tags": ["last-route"],
    },
    {
        "id": "h08",
        "args": [[["GET", "/a", "h1"], ["PUT", "/b", "h2"]], "PUT", "/a"],
        "tags": ["cross-mismatch"],
    },
    {
        "id": "h09",
        "args": [[["GET", "/Users", "h1"], ["GET", "/users", "h2"]], "GET", "/users"],
        "tags": ["case-sensitive"],
    },
    {
        "id": "h10",
        "args": [[["get", "/u", "h1"]], "GET", "/u"],
        "tags": ["case-sensitive", "method-mismatch"],
    },
    {
        "id": "h11",
        "args": [[["GET", "/u/", "h1"], ["GET", "/u", "h2"]], "GET", "/u"],
        "tags": ["trailing-slash"],
    },
    {
        "id": "h12",
        "args": [[["GET", "/*", "wild"]], "GET", "/anything"],
        "tags": ["no-wildcard"],
    },
]

METHODS = ["GET", "POST", "PUT", "DELETE"]
PATHS = ["/", "/a", "/b", "/users", "/users/1"]
HANDLERS = ["h1", "h2", "h3", "h4", "h5", "h6"]


def _next(x):
    return (x * 1103515245 + 12345) % 2147483648


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = _next(x)
        count = (x >> 8) % 7
        routes = []
        for _r in range(count):
            x = _next(x)
            m = METHODS[(x >> 8) % len(METHODS)]
            x = _next(x)
            p = PATHS[(x >> 8) % len(PATHS)]
            x = _next(x)
            h = HANDLERS[(x >> 8) % len(HANDLERS)]
            routes.append([m, p, h])
        # query: half the time pick an existing route's pair, otherwise random
        x = _next(x)
        if routes and (x >> 8) % 2 == 0:
            x = _next(x)
            pick = routes[(x >> 8) % len(routes)]
            method, path = pick[0], pick[1]
        else:
            x = _next(x)
            method = METHODS[(x >> 8) % len(METHODS)]
            x = _next(x)
            path = PATHS[(x >> 8) % len(PATHS)]
        out.append([routes, method, path])
    return out


for _i, _a in enumerate(_lcg(83, 10)):
    HIDDEN.append({"id": f"h{13 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
