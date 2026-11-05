def replace_words(dictionary, sentence):
    root = {}
    for w in dictionary:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True

    def shortest(word):
        node = root
        for i, ch in enumerate(word):
            if ch not in node:
                break
            node = node[ch]
            if "$" in node:
                return word[: i + 1]
        return word

    return " ".join(shortest(w) for w in sentence.split(" "))
