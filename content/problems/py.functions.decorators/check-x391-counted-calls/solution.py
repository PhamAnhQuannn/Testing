import functools


def counted(func):
    """Count calls in wrapper.calls."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


@counted
def double(x):
    return x * 2


def run_counted(xs):
    results = [double(x) for x in xs]
    return [results, double.calls, double.__name__]
