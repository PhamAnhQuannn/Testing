def run_pipeline(steps, xs):
    cur = list(xs)
    for step in steps:
        op = step[0]
        if op == "add":
            k = step[1]
            cur = [x + k for x in cur]
        elif op == "mul":
            k = step[1]
            cur = [x * k for x in cur]
        elif op == "clip":
            lo, hi = step[1], step[2]
            cur = [min(max(x, lo), hi) for x in cur]
    return cur
