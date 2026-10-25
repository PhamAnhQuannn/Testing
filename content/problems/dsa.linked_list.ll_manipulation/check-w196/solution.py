def is_pal_list(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = (slow.next, fast.next.next)
    prev = None
    while slow:
        slow.next, prev, slow = (prev, slow, slow.next)
    a, b = (head, prev)
    while b:
        if a.val != b.val:
            return False
        a, b = (a.next, b.next)
    return True
