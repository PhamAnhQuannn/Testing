def sort_words(words):
    return sorted(words, key=lambda w: (len(w), w))
