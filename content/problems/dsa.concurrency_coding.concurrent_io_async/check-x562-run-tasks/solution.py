def run_tasks(tasks):
    return [t[2] for t in sorted(tasks, key=lambda t: (t[0] + t[1], t[2]))]
