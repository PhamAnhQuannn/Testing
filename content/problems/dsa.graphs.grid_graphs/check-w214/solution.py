def island_perimeter(g):
    p = 0
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j]:
                p += 4
                if i and g[i - 1][j]:
                    p -= 2
                if j and g[i][j - 1]:
                    p -= 2
    return p
