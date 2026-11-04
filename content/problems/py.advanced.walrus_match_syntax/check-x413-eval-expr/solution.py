def evaluate(expr):
    match expr:
        case int(n):
            return n
        case ["add", *args]:
            return sum(evaluate(a) for a in args)
        case ["mul", *args]:
            result = 1
            for a in args:
                result *= evaluate(a)
            return result
        case ["neg", e]:
            return -evaluate(e)
        case ["if", c, a, b]:
            return evaluate(a) if evaluate(c) != 0 else evaluate(b)
        case _:
            return 0
