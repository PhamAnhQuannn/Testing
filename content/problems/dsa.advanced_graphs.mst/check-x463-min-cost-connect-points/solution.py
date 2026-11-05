import heapq


def min_cost_connect_points(points):
    n = len(points)
    seen = [False] * n
    heap = [(0, 0)]
    total = 0
    taken = 0
    while heap and taken < n:
        cost, i = heapq.heappop(heap)
        if seen[i]:
            continue
        seen[i] = True
        total += cost
        taken += 1
        xi, yi = points[i]
        for j in range(n):
            if not seen[j]:
                heapq.heappush(heap, (abs(xi - points[j][0]) + abs(yi - points[j][1]), j))
    return total
