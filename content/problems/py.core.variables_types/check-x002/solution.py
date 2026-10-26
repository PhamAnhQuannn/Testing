def swap_and_describe(n, t):
    n, t = t, n
    return [int(n) + t, type(n).__name__, type(t).__name__]
