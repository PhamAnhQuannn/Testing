def drain_twice(n):
    """Return [first pass, second pass] over one generator of squares 1..n."""

    def squares():
        for i in range(1, n + 1):
            yield i * i

    gen = squares()
    return [list(gen), list(gen)]
