def thread_pool(tasks, workers):
    loads = [0] * workers
    for duration in tasks:
        w = min(range(workers), key=lambda i: loads[i])
        loads[w] += duration
    return loads
