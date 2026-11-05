def critical_connections(n, connections):
    adj = [[] for _ in range(n)]
    for idx, (u, v) in enumerate(connections):
        adj[u].append((v, idx))
        adj[v].append((u, idx))
    disc = [-1] * n
    low = [0] * n
    timer = 0
    bridges = []
    for root in range(n):
        if disc[root] != -1:
            continue
        disc[root] = low[root] = timer
        timer += 1
        # stack frames: [node, parent edge index, next neighbor position]
        stack = [[root, -1, 0]]
        while stack:
            frame = stack[-1]
            node, pe, pos = frame
            if pos < len(adj[node]):
                frame[2] += 1
                nxt, eid = adj[node][pos]
                if eid == pe:
                    continue
                if disc[nxt] == -1:
                    disc[nxt] = low[nxt] = timer
                    timer += 1
                    stack.append([nxt, eid, 0])
                elif disc[nxt] < low[node]:
                    low[node] = disc[nxt]
            else:
                stack.pop()
                if stack:
                    parent = stack[-1][0]
                    if low[node] < low[parent]:
                        low[parent] = low[node]
                    if low[node] > disc[parent]:
                        bridges.append(sorted([parent, node]))
    return sorted(bridges)
