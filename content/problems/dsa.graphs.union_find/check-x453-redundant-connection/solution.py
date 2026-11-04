def redundant_connection(edges):
    n = len(edges)
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    answer = []
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            answer = [u, v]
            continue
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
    return answer
