def errors_per_hour(lines):
    c = {}
    for ln in lines:
        ts, lvl = ln.split()[:2]
        if lvl == "ERROR":
            h = ts.split("T")[1][:2]
            c[h] = c.get(h, 0) + 1
    return dict(sorted(c.items()))
