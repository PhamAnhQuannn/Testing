def dirty_reads(ops):
    uncommitted = {}  # key -> txn đang giữ bản ghi chưa commit
    pairs = []  # (reader, writer) đã đọc dữ liệu chưa commit
    confirmed = set()
    for op in ops:
        kind = op[0]
        if kind == "write":
            uncommitted[op[2]] = op[1]
        elif kind == "read":
            writer = uncommitted.get(op[2])
            if writer is not None and writer != op[1]:
                pairs.append((op[1], writer))
        elif kind == "commit":
            for key in [k for k, w in uncommitted.items() if w == op[1]]:
                del uncommitted[key]
        elif kind == "abort":
            for key in [k for k, w in uncommitted.items() if w == op[1]]:
                del uncommitted[key]
            for reader, writer in pairs:
                if writer == op[1]:
                    confirmed.add(reader)
    return sorted(confirmed)
