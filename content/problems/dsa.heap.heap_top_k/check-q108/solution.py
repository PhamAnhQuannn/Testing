def top_k_words(words, k):
    import heapq
    from collections import Counter

    c = Counter(words)
    return heapq.nsmallest(k, c, key=lambda w: (-c[w], w))
