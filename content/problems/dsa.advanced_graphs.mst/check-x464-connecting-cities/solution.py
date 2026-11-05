def minimum_cost(n, connections):
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    used = 0
    for u, v, c in sorted(connections, key=lambda e: (e[2], e[0], e[1])):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += c
            used += 1
    return total if used == n - 1 else -1
