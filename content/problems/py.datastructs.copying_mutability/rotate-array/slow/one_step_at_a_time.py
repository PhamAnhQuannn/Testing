def rotate(nums: list[int], k: int) -> list[int]:
    result = list(nums)
    n = len(result)
    for _ in range(k % n):
        last = result[n - 1]
        for i in range(n - 1, 0, -1):
            result[i] = result[i - 1]
        result[0] = last
    return result
