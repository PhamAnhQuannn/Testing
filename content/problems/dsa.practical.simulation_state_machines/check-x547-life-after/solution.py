def life_after(board, steps):
    rows = len(board)
    cols = len(board[0]) if rows else 0
    cur = [row[:] for row in board]
    for _ in range(steps):
        nxt = [[0] * cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                n = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if (dr or dc) and 0 <= r + dr < rows and 0 <= c + dc < cols:
                            n += cur[r + dr][c + dc]
                if cur[r][c]:
                    nxt[r][c] = 1 if n in (2, 3) else 0
                else:
                    nxt[r][c] = 1 if n == 3 else 0
        cur = nxt
    return cur
