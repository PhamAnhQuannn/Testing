from typing import get_type_hints


def hint_names(src, name):
    ns = {}
    exec(src, ns)
    hints = get_type_hints(ns[name])
    return [f"{key}:{tp.__name__}" for key, tp in hints.items()]
