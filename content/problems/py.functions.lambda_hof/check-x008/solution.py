def run_pipeline(x, ops):
    table = {
        "inc": lambda v: v + 1,
        "double": lambda v: v * 2,
        "square": lambda v: v * v,
        "neg": lambda v: -v,
    }
    for name in ops:
        x = table[name](x)
    return x
