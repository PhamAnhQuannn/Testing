def max_unique_len(arr):
    masks = []
    for w in arr:
        m = 0
        for ch in w:
            b = 1 << ord(ch) - 97
            if m & b:
                m = -1
                break
            m |= b
        if m != -1:
            masks.append((m, len(w)))
    best = 0

    def go(i, used, total):
        nonlocal best
        best = max(best, total)
        for j in range(i, len(masks)):
            m, ln = masks[j]
            if used & m == 0:
                go(j + 1, used | m, total + ln)

    go(0, 0, 0)
    return best
