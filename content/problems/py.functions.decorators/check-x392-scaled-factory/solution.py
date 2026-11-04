import functools


def scaled(k):
    """Decorator factory: multiply the result by k."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) * k

        return wrapper

    return decorator


def run_scaled(k, xs):
    @scaled(k)
    def add(a, b=0):
        "Add."
        return a + b

    return [[add(x, b=1) for x in xs], add.__name__, add.__doc__]
