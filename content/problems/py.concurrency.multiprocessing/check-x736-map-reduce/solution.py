def count_words(chunks):
    # MAP: per-chunk word counts (each chunk is independent work for one worker).
    partials = []
    for chunk in chunks:
        counts = {}
        for w in chunk:
            counts[w] = counts.get(w, 0) + 1
        partials.append(counts)
    # REDUCE: merge the per-chunk dicts, summing counts of the same word.
    total = {}
    for counts in partials:
        for w, c in counts.items():
            total[w] = total.get(w, 0) + c
    return total
