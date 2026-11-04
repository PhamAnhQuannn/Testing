def apply_ops(nums, specs):
    def add(v, k=1):
        return v + k

    def mul(v, k=2):
        return v * k

    def power(v, k=2):
        return v ** k

    def clip(v, k=10):
        return min(v, k)

    def drop_below(v, k=0):
        return v if v >= k else None

    table = {"add": add, "mul": mul, "pow": power, "clip": clip, "drop_below": drop_below}
    out = list(nums)
    for spec in specs:
        fn = table[spec[0]]
        extra = spec[1:]
        out = [fn(v, *extra) for v in out]
        out = [v for v in out if v is not None]
    return out
