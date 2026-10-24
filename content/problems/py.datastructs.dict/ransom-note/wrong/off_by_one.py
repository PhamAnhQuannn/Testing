from collections import Counter


def can_construct(ransom_note: str, magazine: str) -> bool:
    have = Counter(magazine)
    return all(have[ch] > need for ch, need in Counter(ransom_note).items())
