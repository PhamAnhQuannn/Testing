import types
from collections.abc import Callable
from typing import Any, Optional, Union, get_args, get_origin


def type_format(expr):
    tp = eval(expr, {"Optional": Optional, "Union": Union, "Callable": Callable, "Any": Any})
    return _fmt(tp)


def _fmt(tp):
    if tp is Ellipsis:
        return "..."
    if tp is type(None):
        return "None"
    if isinstance(tp, list):
        return "[" + ", ".join(_fmt(a) for a in tp) + "]"
    origin = get_origin(tp)
    if origin is None:
        return tp.__name__
    args = get_args(tp)
    if origin is Union or origin is types.UnionType:
        return " | ".join(_fmt(a) for a in args)
    return origin.__name__ + "[" + ", ".join(_fmt(a) for a in args) + "]"
