DENOMS = [500, 200, 100, 50]


def dispense(amount):
    result = []
    left = amount
    for denom in DENOMS:
        count = left // denom
        if count > 0:
            result.append([denom, count])
        left = left % denom
    if left != 0 or amount == 0:
        return []
    return result
