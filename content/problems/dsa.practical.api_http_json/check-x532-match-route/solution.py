def match_route(pattern, path):
    pat = pattern.split("/")
    segs = path.split("/")
    if len(pat) != len(segs):
        return None
    params = {}
    for p, s in zip(pat, segs):
        if p.startswith(":"):
            params[p[1:]] = s
        elif p != s:
            return None
    return params
