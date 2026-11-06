def simulate_counter(schedule):
    local = {}
    shared = 0
    for action, tid in schedule:
        if action == "R":
            local[tid] = shared
        else:
            shared = local.get(tid, 0) + 1
    return shared
