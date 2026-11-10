def simplify_order(terms):
    exps = [exp for coeff, exp in terms if coeff > 0]
    return max(exps) if exps else 0
