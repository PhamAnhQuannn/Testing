from collections import deque


def fifo_faults(refs, frames):
    resident = set()
    queue = deque()
    faults = 0
    for page in refs:
        if page in resident:
            continue
        faults += 1
        if len(resident) >= frames:
            old = queue.popleft()
            resident.discard(old)
        resident.add(page)
        queue.append(page)
    return faults
