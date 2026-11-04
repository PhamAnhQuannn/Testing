def is_balanced(r):

    def h(n):
        if not n:
            return 0
        a = h(n.left)
        if a < 0:
            return -1
        b = h(n.right)
        if b < 0 or abs(a - b) > 1:
            return -1
        return 1 + max(a, b)

    return h(r) >= 0
