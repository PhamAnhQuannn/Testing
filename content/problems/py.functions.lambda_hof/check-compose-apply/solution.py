from functools import reduce


def compose_apply(xs, specs):
    makers = {
        "add": lambda n: lambda v: v + n,
        "mul": lambda n: lambda v: v * n,
        "pow": lambda n: lambda v: v**n,
        "mod": lambda n: lambda v: v % n,
        "neg": lambda n: lambda v: -v,
    }
    funcs = [makers[name](n) for name, n in specs]

    def composed(v):
        return reduce(lambda acc, f: f(acc), funcs, v)

    return list(map(composed, xs))
