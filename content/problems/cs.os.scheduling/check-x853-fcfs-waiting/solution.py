def fcfs_waiting(jobs):
    order = sorted(range(len(jobs)), key=lambda i: (jobs[i][0], i))
    wait = [0] * len(jobs)
    t = 0
    for idx in order:
        arrival, burst = jobs[idx]
        start = max(t, arrival)
        wait[idx] = start - arrival
        t = start + burst
    return wait
