def exist(board, word):
    rows = len(board)
    cols = len(board[0]) if rows else 0
    if len(word) > rows * cols:
        return False
    have = {}
    for row in board:
        for ch in row:
            have[ch] = have.get(ch, 0) + 1
    need = {}
    for ch in word:
        need[ch] = need.get(ch, 0) + 1
    for ch, cnt in need.items():
        if have.get(ch, 0) < cnt:
            return False
    grid = [row[:] for row in board]

    def dfs(r, c, k):
        if grid[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        saved = grid[r][c]
        grid[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            inside = 0 <= nr < rows and 0 <= nc < cols
            if inside and grid[nr][nc] != "#" and dfs(nr, nc, k + 1):
                grid[r][c] = saved
                return True
        grid[r][c] = saved
        return False

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
