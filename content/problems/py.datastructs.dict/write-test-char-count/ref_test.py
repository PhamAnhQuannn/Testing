def test_single_char_counted_once():
    assert count_chars("a") == {"a": 1}


def test_repeated_chars():
    assert count_chars("aab") == {"a": 2, "b": 1}
