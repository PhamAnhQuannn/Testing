def max_depth(r):
    return 0 if not r else 1 + max(max_depth(r.left), max_depth(r.right))
