def dispatch(routes, method, path):
    for m, p, h in routes:
        if m == method and p == path:
            return h
    return None
