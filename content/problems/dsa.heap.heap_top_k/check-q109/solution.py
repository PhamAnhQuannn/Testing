def kth_smallest(matrix, k):
    import heapq

    n = len(matrix)
    h = [(matrix[i][0], i, 0) for i in range(n)]
    heapq.heapify(h)
    for _ in range(k - 1):
        v, i, j = heapq.heappop(h)
        if j + 1 < n:
            heapq.heappush(h, (matrix[i][j + 1], i, j + 1))
    return h[0][0]
