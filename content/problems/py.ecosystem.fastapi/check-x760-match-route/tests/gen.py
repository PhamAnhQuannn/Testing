"""Inputs of check-x760-match-route; `expected` comes from solution.py via gen_hidden."""

_R1 = [["/users/{id}", "get_user"], ["/users/{id}/posts/{pid}", "get_post"]]

SAMPLES = [
    {"id": "s1", "args": [_R1, "/users/7/posts/3"]},
    {"id": "s2", "args": [_R1, "/unknown"]},
]

HIDDEN = [
    {"id": "h01", "args": [[], "/users/7"], "tags": ["edge"]},
    {"id": "h02", "args": [[["/", "root"]], "/"], "tags": ["edge"]},
    {"id": "h03", "args": [[["/users/{id}", "get_user"]], "/"], "tags": ["edge"]},
    {
        "id": "h04",
        "args": [[["/health", "health"], ["/users", "list_users"]], "/users"],
        "tags": [],
    },
    {"id": "h05", "args": [_R1, "/users/7"], "tags": []},
    {"id": "h06", "args": [_R1, "/users/7/posts"], "tags": ["edge"]},
    {
        "id": "h07",
        "args": [[["/users/{id}", "get_user"], ["/users/me", "get_me"]], "/users/me"],
        "tags": ["edge"],
    },
    {
        "id": "h08",
        "args": [[["/users/me", "get_me"], ["/users/{id}", "get_user"]], "/users/me"],
        "tags": ["edge"],
    },
    {
        "id": "h09",
        "args": [[["/a/{x}/b/{y}/c/{z}", "deep"]], "/a/1/b/2/c/3"],
        "tags": [],
    },
    {"id": "h10", "args": [[["/a/{x}/b", "ab"]], "/a/1/c"], "tags": ["edge"]},
    {"id": "h11", "args": [[["/items/{id}", "get_item"]], "/items/007"], "tags": []},
    {"id": "h12", "args": [[["/items/{id}", "get_item"]], "/other/5"], "tags": ["edge"]},
    {"id": "h13", "args": [[["/x", "x"]], "/x/y"], "tags": ["edge"]},
]

_LIT = ["users", "items", "posts", "me", "list", "v1"]
_PARAM = ["id", "pid", "name", "slug"]
_VAL = ["1", "7", "abc", "me", "x9", "42"]


def _lcg(seed, n):
    x = seed
    out = []

    def nxt():
        nonlocal x
        x = (x * 1103515245 + 12345) % 2147483648
        return x >> 8

    for _ in range(n):
        routes = []
        for _r in range(nxt() % 5):
            k = 1 + nxt() % 3
            segs = []
            for j in range(k):
                if nxt() % 3 == 0:
                    segs.append("{" + _PARAM[j] + "}")
                else:
                    segs.append(_LIT[nxt() % len(_LIT)])
            routes.append(["/" + "/".join(segs), "h" + str(len(routes))])
        k = 1 + nxt() % 3
        if routes and nxt() % 3 != 0:
            base = routes[nxt() % len(routes)][0].split("/")[1:]
            path = "/" + "/".join(_VAL[nxt() % len(_VAL)] if s.startswith("{") else s for s in base)
        else:
            path = "/" + "/".join(_LIT[nxt() % len(_LIT)] for _j in range(k))
        out.append([routes, path])
    return out


for _i, _a in enumerate(_lcg(23, 12)):
    HIDDEN.append({"id": f"h{14 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
