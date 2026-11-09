def has_deadlock(wait_for):
    graph = {}
    for a, b in wait_for:
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, [])
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}

    def dfs(node):
        color[node] = GRAY
        for nxt in graph[node]:
            if color[nxt] == GRAY:
                return True
            if color[nxt] == WHITE and dfs(nxt):
                return True
        color[node] = BLACK
        return False

    return any(color[node] == WHITE and dfs(node) for node in graph)
