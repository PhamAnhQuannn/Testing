def select_ready(fds, ready):
    ready_set = set(ready)
    return sorted({fd for fd in fds if fd in ready_set})
