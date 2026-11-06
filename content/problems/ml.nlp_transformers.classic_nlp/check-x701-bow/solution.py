def bag_of_words(doc, vocab):
    return [doc.count(w) for w in vocab]
