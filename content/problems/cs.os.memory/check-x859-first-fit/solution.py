def first_fit(blocks, requests):
    remaining = list(blocks)
    result = []
    for req in requests:
        placed = -1
        for i, size in enumerate(remaining):
            if size >= req:
                remaining[i] = size - req
                placed = i
                break
        result.append(placed)
    return result
