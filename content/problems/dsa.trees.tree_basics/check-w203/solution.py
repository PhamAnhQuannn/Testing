def invert(r):
    if r:
        r.left, r.right = (invert(r.right), invert(r.left))
    return r
