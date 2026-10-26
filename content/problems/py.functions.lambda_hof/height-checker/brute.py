def height_checker(heights: list[int]) -> int:
    expected = list(heights)
    n = len(expected)
    for i in range(n):
        smallest = i
        for j in range(i + 1, n):
            if expected[j] < expected[smallest]:
                smallest = j
        expected[i], expected[smallest] = expected[smallest], expected[i]
    count = 0
    for i in range(n):
        if heights[i] != expected[i]:
            count += 1
    return count
