def safe_get(pairs, keys, default):
    d = {}
    for k, v in pairs:
        d[k] = v
    out = []
    for key in keys:
        try:
            out.append(d[key])
        except KeyError:
            out.append(default)
    return out
