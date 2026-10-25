def merge_two(a, b):
    d = cur = ListNode()
    while a and b:
        if a.val <= b.val:
            cur.next, a = (a, a.next)
        else:
            cur.next, b = (b, b.next)
        cur = cur.next
    cur.next = a or b
    return d.next
