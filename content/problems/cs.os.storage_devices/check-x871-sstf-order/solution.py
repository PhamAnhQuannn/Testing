def sstf_order(requests, head):
    pending = list(requests)
    order = []
    pos = head
    while pending:
        best = min(range(len(pending)), key=lambda i: (abs(pending[i] - pos), pending[i]))
        pos = pending.pop(best)
        order.append(pos)
    return order
