class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def build(values, pos):
    nodes = [Node(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if nodes and pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None


def cycle_start(values, pos):
    head = build(values, pos)
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            p = head
            while p is not slow:
                p = p.next
                slow = slow.next
            idx = 0
            cur = head
            while cur is not p:
                cur = cur.next
                idx += 1
            return idx
    return -1
