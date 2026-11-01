def count_chars(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 1) + 1
    return counts
