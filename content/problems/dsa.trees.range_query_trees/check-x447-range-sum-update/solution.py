def range_sum_updates(nums, ops):
    n = len(nums)
    cur = list(nums)
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] += cur[i - 1]
        j = i + (i & -i)
        if j <= n:
            tree[j] += tree[i]

    def add(i, delta):
        i += 1
        while i <= n:
            tree[i] += delta
            i += i & -i

    def prefix(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    out = []
    for op in ops:
        if op[0] == "u":
            i, v = op[1], op[2]
            add(i, v - cur[i])
            cur[i] = v
        else:
            out.append(prefix(op[2] + 1) - prefix(op[1]))
    return out
