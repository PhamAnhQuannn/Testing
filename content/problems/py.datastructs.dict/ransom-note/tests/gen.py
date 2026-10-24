"""Hidden-test inputs for ransom-note; tools/gen_hidden.py computes `expected` from solution.py."""

import random
import string

SEED = 383
BIG = 10**5


def _shuffled(rng, text):
    letters = list(text)
    rng.shuffle(letters)
    return "".join(letters)


def hidden_inputs():
    rng = random.Random(SEED)
    alphabet = string.ascii_lowercase
    small_rng = random.Random(1)
    small_magazine = "".join(small_rng.choices("abcde", k=20))
    small_note = _shuffled(small_rng, "".join(small_rng.sample(small_magazine, 12)))
    # Every letter appears, so a missing one cannot be the reason for `false` below.
    big_magazine = "".join(rng.choices(alphabet, k=BIG - len(alphabet))) + alphabet
    big_note = _shuffled(rng, big_magazine)
    return [
        {"id": "h01", "args": ["abc", "ab"], "tags": ["edge"]},
        {"id": "h02", "args": ["", "abc"], "tags": ["edge", "empty"]},
        {"id": "h03", "args": ["a", ""], "tags": ["edge", "empty"]},
        {"id": "h04", "args": ["aabbc", "cbbaa"], "tags": []},
        {"id": "h05", "args": ["aab", "ab"], "tags": ["edge"]},
        {"id": "h06", "args": ["xyz", "xyz"], "tags": ["edge"]},
        {"id": "h07", "args": ["ab", "zzzabzzz"], "tags": []},
        {"id": "h08", "args": [alphabet, alphabet[::-1]], "tags": []},
        {"id": "h09", "args": ["a" * 50, "a" * 49], "tags": ["edge"]},
        {"id": "h10", "args": [small_note, small_magazine], "tags": ["random"]},
        {"id": "h11", "args": [big_note, big_magazine], "tags": ["stress"]},
        {"id": "h12", "args": [big_note, big_magazine[:-1]], "tags": ["stress"]},
    ]


def small_inputs(seed, n):
    """`n` argument lists with at most 12 characters per string, for the brute-force cross-check."""
    rng = random.Random(seed)
    return [["".join(rng.choices("abc", k=rng.randint(0, 12))) for _ in range(2)] for _ in range(n)]
