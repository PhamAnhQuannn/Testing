def apply_locked_ops(ops):
    holder = None
    counter = 0
    for op, tid in ops:
        if op == "acq" and holder is None:
            holder = tid
        elif op == "inc" and holder == tid:
            counter += 1
        elif op == "rel" and holder == tid:
            holder = None
    return counter
