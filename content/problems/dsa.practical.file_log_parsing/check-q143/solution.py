def top_paths(lines, n):
    from collections import Counter

    c = Counter()
    for ln in lines:
        p = ln.split()
        if len(p) == 3 and p[2].isdigit():
            c[p[1]] += 1
    return sorted(c.items(), key=lambda x: (-x[1], x[0]))[:n]
