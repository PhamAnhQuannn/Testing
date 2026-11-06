OPS = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "max": lambda a, b: a if a >= b else b,
    "min": lambda a, b: a if a <= b else b,
}


def apply_op(op, a, b):
    return OPS.get(op, lambda x, y: 0)(a, b)
