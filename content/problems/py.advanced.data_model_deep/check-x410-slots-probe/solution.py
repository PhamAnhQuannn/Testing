class Base:
    pass


def slots_probe(fields, attempts, with_dict):
    bases = (Base,) if with_dict else ()
    probe_cls = type("Probe", bases, {"__slots__": tuple(fields)})
    obj = probe_cls()
    results = []
    for name in attempts:
        try:
            setattr(obj, name, 1)
            results.append("ok")
        except AttributeError:
            results.append("blocked")
    return [results, hasattr(obj, "__dict__")]
