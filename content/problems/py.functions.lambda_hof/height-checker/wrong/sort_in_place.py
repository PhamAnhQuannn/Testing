def height_checker(heights: list[int]) -> int:
    expected = heights
    expected.sort()
    return sum(1 for a, b in zip(heights, expected, strict=True) if a != b)
