def generate(num_rows: int) -> list[list[int]]:
    triangle = []
    row = [1]
    for _ in range(num_rows):
        triangle.append(row)  # the same list object every time
        row.append(1)
        for j in range(len(row) - 2, 0, -1):
            row[j] = row[j] + row[j - 1]
    return triangle
