def semaphore(ops, initial):
    count = initial
    blocked = 0
    for op in ops:
        if op == "V":
            count += 1
        elif count > 0:
            count -= 1
        else:
            blocked += 1
    return [count, blocked]
