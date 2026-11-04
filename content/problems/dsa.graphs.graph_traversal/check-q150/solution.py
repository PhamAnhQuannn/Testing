def is_bipartite(graph):
    color = {}
    for s in range(len(graph)):
        if s in color:
            continue
        color[s] = 0
        q = [s]
        while q:
            u = q.pop()
            for v in graph[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True
