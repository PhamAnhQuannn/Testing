def count_pal_substrings(s):
    n = len(s)
    c = 0
    for ctr in range(2 * n - 1):
        l, r = (ctr // 2, ctr // 2 + ctr % 2)
        while l >= 0 and r < n and (s[l] == s[r]):
            c += 1
            l -= 1
            r += 1
    return c
