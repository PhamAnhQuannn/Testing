def apply_merge(tokens, pair):
    out = []
    i = 0
    n = len(tokens)
    while i < n:
        if i + 1 < n and tokens[i] == pair[0] and tokens[i + 1] == pair[1]:
            out.append(pair[0] + pair[1])
            i += 2
        else:
            out.append(tokens[i])
            i += 1
    return out
