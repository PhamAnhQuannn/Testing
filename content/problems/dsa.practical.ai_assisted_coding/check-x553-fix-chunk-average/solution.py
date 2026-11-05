def chunk_averages(nums, size):
    if size <= 0 or not nums:
        return []
    out = []
    for i in range(0, len(nums), size):
        chunk = nums[i : i + size]
        total, n = sum(chunk), len(chunk)
        out.append(total // n if total % n == 0 else total / n)
    return out
