from collections import deque


def count_reachable(n, edges, src):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    seen = [False] * n
    seen[src] = True
    q = deque([src])
    count = 1
    while q:
        u = q.popleft()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                count += 1
                q.append(v)
    return count
