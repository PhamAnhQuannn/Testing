def length_of_last_word(s: str) -> int:
    return len(s) - s.rfind(" ") - 1
