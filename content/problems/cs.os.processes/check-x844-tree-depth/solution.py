def tree_depth(edges):
    parent = {pid: ppid for pid, ppid in edges}
    memo = {}
    best = 0
    for pid in parent:
        path = []
        cur = pid
        while cur in parent and cur not in memo:
            path.append(cur)
            cur = parent[cur]
        depth = memo.get(cur, 0)
        for node in reversed(path):
            depth += 1
            memo[node] = depth
        best = max(best, memo[pid])
    return best
