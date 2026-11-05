def min_path_sum(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [0] * cols
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                dp[c] = grid[0][0]
            elif r == 0:
                dp[c] = dp[c - 1] + grid[r][c]
            elif c == 0:
                dp[c] = dp[c] + grid[r][c]
            else:
                dp[c] = min(dp[c], dp[c - 1]) + grid[r][c]
    return dp[-1]
