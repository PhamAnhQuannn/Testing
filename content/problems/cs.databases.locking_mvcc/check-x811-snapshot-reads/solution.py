from bisect import bisect_right


def snapshot_reads(versions, read_tss):
    tss = [v[0] for v in versions]
    out = []
    for ts in read_tss:
        i = bisect_right(tss, ts)
        out.append(None if i == 0 else versions[i - 1][1])
    return out
