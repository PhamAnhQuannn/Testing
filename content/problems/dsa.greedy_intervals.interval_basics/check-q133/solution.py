def insert_interval(iv, new):
    res = []
    i = 0
    while i < len(iv) and iv[i][1] < new[0]:
        res.append(iv[i])
        i += 1
    while i < len(iv) and iv[i][0] <= new[1]:
        new = [min(new[0], iv[i][0]), max(new[1], iv[i][1])]
        i += 1
    res.append(new)
    return res + iv[i:]
