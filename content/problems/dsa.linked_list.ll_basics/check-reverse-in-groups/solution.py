class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def reverse_in_groups(vals, k):
    dummy = Node(0)
    cur = dummy
    for v in vals:
        cur.next = Node(v)
        cur = cur.next
    prev_tail = dummy
    while True:
        probe = prev_tail.next
        cnt = 0
        while probe and cnt < k:
            probe = probe.next
            cnt += 1
        if cnt < k:
            break
        first = prev_tail.next
        prev, node = probe, first
        for _ in range(k):
            nxt = node.next
            node.next = prev
            prev = node
            node = nxt
        prev_tail.next = prev
        prev_tail = first
    out = []
    cur = dummy.next
    while cur:
        out.append(cur.val)
        cur = cur.next
    return out
