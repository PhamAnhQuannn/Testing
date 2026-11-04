def is_valid_bst(r, lo=float("-inf"), hi=float("inf")):
    if not r:
        return True
    if not lo < r.val < hi:
        return False
    return is_valid_bst(r.left, lo, r.val) and is_valid_bst(r.right, r.val, hi)
