def erase_overlap(iv):
    iv = sorted(iv, key=lambda x: x[1])
    end = float("-inf")
    keep = 0
    for a, b in iv:
        if a >= end:
            keep += 1
            end = b
    return len(iv) - keep
