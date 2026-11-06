"""Input generator for check-x685-logistic-proba; expected values come from solution.py."""


def sample_inputs():
    return [
        {"id": "s1", "args": [[0.0], 0.0, [5.0]]},
        {"id": "s2", "args": [[0.5, 1.0], -1.0, [2.0, 1.0]]},
    ]


def hidden_inputs():
    return [
        {"id": "h01", "args": [[1.0], 0.0, [0.0]], "tags": ["edge"]},
        {"id": "h02", "args": [[2.0, -2.0], 0.0, [1.0, 1.0]], "tags": ["edge"]},
        {"id": "h03", "args": [[1.0], 0.0, [1000.0]], "tags": ["edge"]},
        {"id": "h04", "args": [[1.0], 0.0, [-1000.0]], "tags": ["edge"]},
        {"id": "h05", "args": [[1.0, 1.0], 0.0, [1.0, 1.0]], "tags": ["basic"]},
        {"id": "h06", "args": [[-1.0, -1.0], 0.0, [1.0, 1.0]], "tags": ["basic"]},
        {"id": "h07", "args": [[0.0, 0.0, 0.0], 0.5, [3.0, 4.0, 5.0]], "tags": ["bias"]},
        {"id": "h08", "args": [[1.5, -0.5, 2.0], -1.0, [1.0, 2.0, 0.5]], "tags": ["basic"]},
        {
            "id": "h09",
            "args": [[0.1, 0.2, 0.3, 0.4], 0.05, [1.0, 2.0, 3.0, 4.0]],
            "tags": ["basic"],
        },
        {"id": "h10", "args": [[10.0, 10.0], -30.0, [1.0, 1.0]], "tags": ["negative"]},
        {"id": "h11", "args": [[-3.5], 2.0, [4.0]], "tags": ["negative"]},
        {"id": "h12", "args": [[0.001, -0.002], 0.0, [10.0, 5.0]], "tags": ["small"]},
    ]


def small_inputs(seed, n):
    state = seed % 2147483648
    out = []

    def nxt():
        nonlocal state
        state = (1103515245 * state + 12345) % 2147483648
        return state / 2147483648.0

    for i in range(n):
        d = 1 + int(nxt() * 5)
        weights = [round(nxt() * 8 - 4, 3) for _ in range(d)]
        x = [round(nxt() * 20 - 10, 3) for _ in range(d)]
        bias = round(nxt() * 10 - 5, 3)
        out.append({"id": f"r{i}", "args": [weights, bias, x], "tags": ["random"]})
    return out
