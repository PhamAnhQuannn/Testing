def can_construct(ransom_note: str, magazine: str) -> bool:
    return all(ransom_note.count(ch) <= magazine.count(ch) for ch in ransom_note)
