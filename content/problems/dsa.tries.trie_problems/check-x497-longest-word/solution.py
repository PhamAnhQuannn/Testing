def longest_word(words):
    built = {""}
    best = ""
    for w in sorted(set(words)):
        if w[:-1] in built:
            built.add(w)
            if len(w) > len(best):
                best = w
    return best
