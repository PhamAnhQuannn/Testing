def merge_intervals(pairs):
    out = []
    for start, end in sorted(pairs):
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out
