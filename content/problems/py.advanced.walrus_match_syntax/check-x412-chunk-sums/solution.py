def chunk_sums(data, k):
    out = []
    i = 0
    while chunk := data[i : i + k]:
        out.append(sum(chunk))
        i += k
    return out
