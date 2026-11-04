import heapq


def median_doubled(nums):
    lo, hi = [], []  # lo: max-heap (negated), hi: min-heap
    out = []
    for x in nums:
        heapq.heappush(lo, -x)
        heapq.heappush(hi, -heapq.heappop(lo))
        if len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        if len(lo) > len(hi):
            out.append(-2 * lo[0])
        else:
            out.append(-lo[0] + hi[0])
    return out
