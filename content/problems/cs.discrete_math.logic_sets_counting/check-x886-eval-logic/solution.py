def eval_logic(expr):
    if isinstance(expr, bool):
        return expr
    op = expr[0]
    operands = expr[1:]
    if op == "not":
        return not eval_logic(operands[0])
    if op == "and":
        return all(eval_logic(o) for o in operands)
    if op == "or":
        return any(eval_logic(o) for o in operands)
