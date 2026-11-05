def eval_expr(expr):
    toks = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            toks.append(expr[i:j])
            i = j
        elif c in "+-*/()":
            toks.append(c)
            i += 1
        else:
            i += 1

    pos = 0

    def peek():
        return toks[pos] if pos < len(toks) else None

    def take():
        nonlocal pos
        pos += 1
        return toks[pos - 1]

    def parse_expr():
        v = parse_term()
        while peek() in ("+", "-"):
            op = take()
            r = parse_term()
            v = v + r if op == "+" else v - r
        return v

    def parse_term():
        v = parse_factor()
        while peek() in ("*", "/"):
            op = take()
            r = parse_factor()
            v = v * r if op == "*" else int(v / r)
        return v

    def parse_factor():
        t = take()
        if t == "(":
            v = parse_expr()
            take()
            return v
        return int(t)

    return parse_expr()
