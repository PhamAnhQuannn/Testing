def car_pooling(trips, capacity):
    ev = []
    for n, a, b in trips:
        ev += [(a, n), (b, -n)]
    cur = 0
    for _, d in sorted(ev):
        cur += d
        if cur > capacity:
            return False
    return True
