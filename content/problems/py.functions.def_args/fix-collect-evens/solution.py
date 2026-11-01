def collect_evens(nums, acc=None):
    if acc is None:
        acc = []
    for n in nums:
        if n % 2 == 0:
            acc.append(n)
    return acc


def evens_per_batch(batches):
    return [collect_evens(batch) for batch in batches]
