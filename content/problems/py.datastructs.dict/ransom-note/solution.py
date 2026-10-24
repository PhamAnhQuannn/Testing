def can_construct(ransom_note: str, magazine: str) -> bool:
    have = {}
    for ch in magazine:
        have[ch] = have.get(ch, 0) + 1
    for ch in ransom_note:
        if have.get(ch, 0) == 0:
            return False
        have[ch] -= 1
    return True
