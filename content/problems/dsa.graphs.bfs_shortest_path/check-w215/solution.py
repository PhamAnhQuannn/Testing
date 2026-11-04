def path_cells(g):
    from collections import deque

    R, C = (len(g), len(g[0]))
    if g[0][0] or g[R - 1][C - 1]:
        return -1
    q = deque([(0, 0, 1)])
    seen = {(0, 0)}
    while q:
        r, c, d = q.popleft()
        if (r, c) == (R - 1, C - 1):
            return d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = (r + dr, c + dc)
            if 0 <= nr < R and 0 <= nc < C and (not g[nr][nc]) and ((nr, nc) not in seen):
                seen.add((nr, nc))
                q.append((nr, nc, d + 1))
    return -1
