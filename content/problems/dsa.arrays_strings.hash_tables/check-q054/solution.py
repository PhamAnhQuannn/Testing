def group_anagrams(words):
    g = {}
    for w in words:
        g.setdefault("".join(sorted(w)), []).append(w)
    return sorted((sorted(v) for v in g.values()))
