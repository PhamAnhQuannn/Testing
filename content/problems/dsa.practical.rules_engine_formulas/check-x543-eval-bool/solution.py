def eval_bool(expr):
    tokens = expr.split()
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def or_expr():
        nonlocal pos
        value = and_expr()
        while peek() == "OR":
            pos += 1
            rhs = and_expr()
            value = value or rhs
        return value

    def and_expr():
        nonlocal pos
        value = not_expr()
        while peek() == "AND":
            pos += 1
            rhs = not_expr()
            value = value and rhs
        return value

    def not_expr():
        nonlocal pos
        if peek() == "NOT":
            pos += 1
            return not not_expr()
        return atom()

    def atom():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        if tok == "(":
            value = or_expr()
            pos += 1  # skip ")"
            return value
        return tok == "T"

    return bool(or_expr())
