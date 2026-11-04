def spiral(m):
    res = []
    while m:
        res += m.pop(0)
        m = [list(r) for r in zip(*m)][::-1]
    return res
