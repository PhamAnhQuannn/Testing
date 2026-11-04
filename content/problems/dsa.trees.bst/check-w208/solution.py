def lca_bst(r, p, q):
    while r:
        if p < r.val and q < r.val:
            r = r.left
        elif p > r.val and q > r.val:
            r = r.right
        else:
            return r.val
