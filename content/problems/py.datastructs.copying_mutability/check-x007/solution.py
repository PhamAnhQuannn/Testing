def plus_one_copy(grid):
    new_grid = []
    for row in grid:
        new_row = []
        for v in row:
            new_row.append(v + 1)
        new_grid.append(new_row)
    return [new_grid, grid]
