def has_path(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = {s}
    st = [s]
    while st:
        u = st.pop()
        if u == t:
            return True
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                st.append(v)
    return False
