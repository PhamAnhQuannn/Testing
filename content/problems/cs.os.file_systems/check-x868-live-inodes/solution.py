def live_inodes(ops):
    name_to_inode = {}
    ref = {}
    next_id = 0
    for op in ops:
        kind = op[0]
        if kind == "create":
            name = op[1]
            name_to_inode[name] = next_id
            ref[next_id] = 1
            next_id += 1
        elif kind == "link":
            new_name, existing = op[1], op[2]
            if existing in name_to_inode:
                inode = name_to_inode[existing]
                name_to_inode[new_name] = inode
                ref[inode] += 1
        elif kind == "unlink":
            name = op[1]
            if name in name_to_inode:
                inode = name_to_inode.pop(name)
                ref[inode] -= 1
    return sum(1 for c in ref.values() if c > 0)
