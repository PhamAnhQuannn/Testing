import heapq


def running_kth_largest(nums: list[int], k: int) -> list[int]:
    heap = []
    result = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
        result.append(heap[0] if len(heap) >= k - 1 and heap else -1)
    return result
