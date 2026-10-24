def duplicate_zeros(arr):
    expanded = []
    for x in arr:
        expanded.append(x)
        if x == 0:
            expanded.append(0)
    arr[:] = expanded[: len(arr)]
