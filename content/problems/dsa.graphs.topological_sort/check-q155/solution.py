def can_finish(n, prereqs):
    from collections import deque

    adj = [[] for _ in range(n)]
    deg = [0] * n
    for a, b in prereqs:
        adj[b].append(a)
        deg[a] += 1
    q = deque((i for i in range(n) if deg[i] == 0))
    seen = 0
    while q:
        u = q.popleft()
        seen += 1
        for v in adj[u]:
            deg[v] -= 1
            if deg[v] == 0:
                q.append(v)
    return seen == n
