def can_construct(ransom_note: str, magazine: str) -> bool:
    remaining = list(magazine)
    for ch in ransom_note:
        if ch not in remaining:
            return False
        remaining.remove(ch)
    return True
