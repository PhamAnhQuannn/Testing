import heapq


def merge_k(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heap.append((lst[0], i, 0))
    heapq.heapify(heap)
    out = []
    while heap:
        val, i, j = heapq.heappop(heap)
        out.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out
