def parse_ints(tokens):
    result = []
    for token in tokens:
        try:
            n = int(token)
        except ValueError:
            continue
        result.append(n)
    return result
