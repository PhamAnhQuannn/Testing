from collections import deque


def sliding_window_max(nums, k):
    if not nums or k <= 0:
        return []
    if k >= len(nums):
        return [max(nums)]
    dq = deque()  # indices, values decreasing
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
