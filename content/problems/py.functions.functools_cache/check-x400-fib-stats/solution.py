from functools import cache


def fib_stats(n):
    @cache
    def fib(k):
        return k if k < 2 else fib(k - 1) + fib(k - 2)

    value = fib(n)
    info = fib.cache_info()
    return [value, info.hits, info.misses]
