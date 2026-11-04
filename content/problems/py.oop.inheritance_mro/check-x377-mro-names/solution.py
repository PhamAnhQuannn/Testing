def mro_names(spec):
    """spec: list of [name, [base names]]; return MRO names of the last class, or ["error"]."""
    made = {}
    try:
        for name, bases in spec:
            made[name] = type(name, tuple(made[b] for b in bases), {})
    except TypeError:
        return ["error"]
    last = made[spec[-1][0]]
    return [c.__name__ for c in last.__mro__ if c is not object]
