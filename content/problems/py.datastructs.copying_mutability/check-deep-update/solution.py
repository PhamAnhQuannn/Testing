def deep_update(grid, cells):
    new = [row[:] for row in grid]
    for r, c, v in cells:
        new[r][c] = v
    return [new, grid]
