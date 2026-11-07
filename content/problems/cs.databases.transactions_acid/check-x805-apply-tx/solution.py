def apply_tx(ops):
    committed = {}
    working = {}
    in_tx = False
    for op in ops:
        kind = op[0]
        if kind == "set":
            if in_tx:
                working[op[1]] = op[2]
            else:
                committed[op[1]] = op[2]
        elif kind == "begin":
            if not in_tx:
                in_tx = True
                working = dict(committed)
        elif kind == "commit":
            if in_tx:
                committed = working
                working = {}
                in_tx = False
        elif kind == "rollback" and in_tx:
            working = {}
            in_tx = False
    return [[k, v] for k, v in sorted(committed.items())]
