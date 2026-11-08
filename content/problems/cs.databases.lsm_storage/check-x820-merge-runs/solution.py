def merge_runs(runs):
    merged = {}
    for run in runs:
        for key, value in run:
            merged[key] = value
    return [[k, merged[k]] for k in sorted(merged)]
