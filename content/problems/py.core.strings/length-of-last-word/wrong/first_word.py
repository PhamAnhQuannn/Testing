def length_of_last_word(s: str) -> int:
    t = s.strip()
    pos = t.find(" ")
    if pos == -1:
        return len(t)
    return pos
