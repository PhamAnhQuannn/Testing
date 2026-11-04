import heapq


def min_cost_ropes(weights):
    h = list(weights)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        s = heapq.heappop(h) + heapq.heappop(h)
        total += s
        heapq.heappush(h, s)
    return total
