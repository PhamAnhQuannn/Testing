def eventual_safe_nodes(graph):
    n = len(graph)
    rev = [[] for _ in range(n)]
    outdeg = [len(graph[i]) for i in range(n)]
    for u in range(n):
        for v in graph[u]:
            rev[v].append(u)
    stack = [i for i in range(n) if outdeg[i] == 0]
    safe = [False] * n
    while stack:
        v = stack.pop()
        safe[v] = True
        for u in rev[v]:
            outdeg[u] -= 1
            if outdeg[u] == 0:
                stack.append(u)
    return [i for i in range(n) if safe[i]]
