import statistics


def stats_summary(nums):
    return [
        round(statistics.mean(nums), 2),
        round(float(statistics.median(nums)), 2),
        statistics.mode(nums),
    ]
