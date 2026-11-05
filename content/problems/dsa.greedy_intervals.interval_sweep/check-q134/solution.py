def min_arrows(points):
    pts = sorted(points, key=lambda p: p[1])
    n = 0
    end = float("-inf")
    for a, b in pts:
        if a > end:
            n += 1
            end = b
    return n
