def top_n_words(text, n):
    import re
    from collections import Counter

    c = Counter(re.findall("[a-z0-9']+", text.lower()))
    return sorted(c.items(), key=lambda x: (-x[1], x[0]))[:n]
