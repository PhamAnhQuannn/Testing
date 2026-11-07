from collections import deque


def event_loop_order(tasks):
    q = deque((t[0], t[1]) for t in tasks)
    trace = []
    while q:
        tid, left = q.popleft()
        trace.append(tid)
        if left > 1:
            q.append((tid, left - 1))
    return trace
