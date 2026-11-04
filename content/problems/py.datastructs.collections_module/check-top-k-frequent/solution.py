from collections import Counter


def top_k_frequent(words, k):
    cnt = Counter(words)
    order = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
    return [w for w, _ in order[:k]]
