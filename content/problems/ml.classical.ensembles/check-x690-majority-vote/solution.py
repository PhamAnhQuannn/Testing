def majority_vote(predictions):
    n_models = len(predictions)
    n_samples = len(predictions[0])
    result = []
    for j in range(n_samples):
        counts = {}
        for m in range(n_models):
            label = predictions[m][j]
            counts[label] = counts.get(label, 0) + 1
        best = min(counts, key=lambda lab: (-counts[lab], lab))
        result.append(best)
    return result
