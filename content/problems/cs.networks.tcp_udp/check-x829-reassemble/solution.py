def reassemble(segments):
    out = []
    nxt = 0
    for seq, data in sorted(segments, key=lambda s: s[0]):
        if seq == nxt:
            out.append(data)
            nxt += len(data)
        elif seq > nxt:
            break
    return "".join(out)
