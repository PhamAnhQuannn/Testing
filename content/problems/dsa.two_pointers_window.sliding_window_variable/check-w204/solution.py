def char_replacement(s, k):
    from collections import defaultdict

    c = defaultdict(int)
    l = best = mx = 0
    for r, ch in enumerate(s):
        c[ch] += 1
        mx = max(mx, c[ch])
        while r - l + 1 - mx > k:
            c[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best
