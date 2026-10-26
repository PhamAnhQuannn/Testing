def generate(num_rows: int) -> list[list[int]]:
    return [[1] * (i + 1) for i in range(num_rows)]
