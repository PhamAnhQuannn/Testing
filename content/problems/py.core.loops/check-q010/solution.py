def count_vowels(s):
    c = 0
    for ch in s.lower():
        if ch in "aeiou":
            c += 1
    return c
