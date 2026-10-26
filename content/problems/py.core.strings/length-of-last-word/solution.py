def length_of_last_word(s: str) -> int:
    t = s.rstrip()
    return len(t) - t.rfind(" ") - 1
