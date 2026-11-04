from itertools import islice


def first_evens(nums, k):
    """Return the first k even numbers of nums using a lazy generator."""

    def evens():
        for x in nums:
            if x % 2 == 0:
                yield x

    return list(islice(evens(), k))
