def match_route(routes, path):
    segs = path.split("/")
    for pattern, handler in routes:
        parts = pattern.split("/")
        if len(parts) != len(segs):
            continue
        params = {}
        ok = True
        for p, s in zip(parts, segs):
            if len(p) >= 2 and p.startswith("{") and p.endswith("}"):
                params[p[1:-1]] = s
            elif p != s:
                ok = False
                break
        if ok:
            return [handler, params]
    return []
