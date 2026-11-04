def last_stone(stones):
    import heapq

    h = [-s for s in stones]
    heapq.heapify(h)
    while len(h) > 1:
        a, b = (heapq.heappop(h), heapq.heappop(h))
        if a != b:
            heapq.heappush(h, a - b)
    return -h[0] if h else 0
