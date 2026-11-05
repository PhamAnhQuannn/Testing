from math import gcd


def max_points(points):
    n = len(points)
    if n <= 2:
        return n
    best = 1
    for i in range(n):
        counts = {}
        dup = 0
        local = 0
        for j in range(i + 1, n):
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            if dx == 0 and dy == 0:
                dup += 1
                continue
            g = gcd(abs(dx), abs(dy))
            dx //= g
            dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            key = (dy, dx)
            counts[key] = counts.get(key, 0) + 1
            if counts[key] > local:
                local = counts[key]
        best = max(best, local + dup + 1)
    return best
