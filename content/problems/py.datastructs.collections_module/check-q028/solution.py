def top_words(words, k):
    from collections import Counter

    c = Counter(words)
    return sorted(c, key=lambda w: (-c[w], w))[:k]
