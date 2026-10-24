def can_construct(ransom_note: str, magazine: str) -> bool:
    return set(ransom_note) <= set(magazine)
