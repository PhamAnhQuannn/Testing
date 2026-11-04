def set_zeroes(m):
    rows = {i for i, r in enumerate(m) if 0 in r}
    cols = {j for r in m for j, v in enumerate(r) if v == 0}
    for i in range(len(m)):
        for j in range(len(m[0])):
            if i in rows or j in cols:
                m[i][j] = 0
    return m
