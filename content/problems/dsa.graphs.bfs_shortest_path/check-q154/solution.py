def rotting(grid):
    from collections import deque

    R, Cc = (len(grid), len(grid[0]))
    q = deque()
    fresh = 0
    for i in range(R):
        for j in range(Cc):
            if grid[i][j] == 2:
                q.append((i, j, 0))
            elif grid[i][j] == 1:
                fresh += 1
    t = 0
    while q:
        r, c, t = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = (r + dr, c + dc)
            if 0 <= nr < R and 0 <= nc < Cc and (grid[nr][nc] == 1):
                grid[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc, t + 1))
    return t if fresh == 0 else -1
