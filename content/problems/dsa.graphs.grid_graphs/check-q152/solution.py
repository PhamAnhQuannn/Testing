def max_area(grid):
    R, Cc = (len(grid), len(grid[0]))
    best = 0
    for i in range(R):
        for j in range(Cc):
            if grid[i][j] == 1:
                st = [(i, j)]
                grid[i][j] = 0
                a = 0
                while st:
                    r, c = st.pop()
                    a += 1
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = (r + dr, c + dc)
                        if 0 <= nr < R and 0 <= nc < Cc and (grid[nr][nc] == 1):
                            grid[nr][nc] = 0
                            st.append((nr, nc))
                best = max(best, a)
    return best
