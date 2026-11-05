def total_size(node):
    kind = node[0]
    if kind == "file":
        return node[2]
    total = 0
    for child in node[2]:
        total += total_size(child)
    return total
