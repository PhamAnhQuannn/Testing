"""Inputs of check-x532-match-route; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": ["/users/:id", "/users/7"]},
    {"id": "s2", "args": ["/users/:id", "/posts/7"]},
    {"id": "s3", "args": ["/a/b", "/a/b"]},
]


def _deep(seed, n):
    """Pattern/path pair with n segments; every third segment is a parameter."""
    x = seed
    pat = []
    path = []
    for i in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        word = "s" + str((x >> 8) % 100)
        if i % 3 == 0:
            pat.append(":p" + str(i))
        else:
            pat.append(word)
        path.append(word)
    return "/" + "/".join(pat), "/" + "/".join(path)


_p1, _q1 = _deep(1, 12)
_p2, _q2 = _deep(2, 40)

HIDDEN = [
    {"id": "h01", "args": ["/users/:id", "/users/7"], "tags": []},
    {"id": "h02", "args": ["/users/:id", "/users"], "tags": ["edge"]},
    {"id": "h03", "args": ["/users/:id", "/users/7/posts"], "tags": ["edge"]},
    {"id": "h04", "args": ["/users/:id", "/accounts/7"], "tags": ["edge"]},
    {"id": "h05", "args": ["/a/b/c", "/a/b/c"], "tags": ["edge"]},
    {"id": "h06", "args": ["/a/b/c", "/a/b/d"], "tags": ["edge"]},
    {"id": "h07", "args": ["/users/:uid/posts/:pid", "/users/3/posts/99"], "tags": []},
    {"id": "h08", "args": ["/users/:uid/posts/:pid", "/users/3/comments/99"], "tags": []},
    {"id": "h09", "args": ["/", "/"], "tags": ["edge"]},
    {"id": "h10", "args": ["/users/:id", "/users/7/"], "tags": ["edge"]},
    {"id": "h11", "args": ["/:a/:b", "/x/y"], "tags": []},
    {"id": "h12", "args": [_p1, _q1], "tags": []},
    {"id": "h13", "args": [_p2, _q2], "tags": []},
    {"id": "h14", "args": [_p2, _q2 + "/extra"], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
