def test_element_not_used_twice():
    assert two_sum([3, 2, 4], 6) == [1, 2]


def test_duplicate_values():
    assert two_sum([3, 3], 6) == [0, 1]
