def count_provinces(is_connected):
    n = len(is_connected)
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    count = n
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                ri, rj = find(i), find(j)
                if ri != rj:
                    if size[ri] < size[rj]:
                        ri, rj = rj, ri
                    parent[rj] = ri
                    size[ri] += size[rj]
                    count -= 1
    return count
