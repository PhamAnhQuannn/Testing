def gen_paren(n):
    res = []

    def go(s, o, c):
        if len(s) == 2 * n:
            res.append(s)
            return
        if o < n:
            go(s + "(", o + 1, c)
        if c < o:
            go(s + ")", o, c + 1)

    go("", 0, 0)
    return sorted(res)
