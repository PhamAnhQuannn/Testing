def shortest(n, edges, s, t):
    from collections import deque

    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            return dist[u]
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return -1
