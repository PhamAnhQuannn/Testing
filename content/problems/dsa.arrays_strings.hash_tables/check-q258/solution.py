def most_common(words):
    cnt = {}
    for w in words:
        cnt[w] = cnt.get(w, 0) + 1
    best = ""
    for w, c in cnt.items():
        if best == "" or c > cnt[best] or (c == cnt[best] and w < best):
            best = w
    return best
