"""Inputs of check-x418-run-main-guard.

`expected` is recorded from solution.py by tools/gen_hidden.py.
"""

SAMPLES = [
    {"id": "s1", "args": ["if __name__ == '__main__':\n    log.append('run')"]},
    {"id": "s2", "args": ["log.append('top')"]},
    {"id": "s3", "args": ["log.append(__name__)"]},
]

HIDDEN = [
    {"id": "h01", "args": [""], "tags": ["edge"]},
    {"id": "h02", "args": ["log.append(1)\nlog.append(2)"], "tags": []},
    {"id": "h03", "args": ["if __name__ != '__main__':\n    log.append('imported')"], "tags": []},
    {
        "id": "h04",
        "args": [
            "log.append('a')\nif __name__ == '__main__':\n    log.append('main')\nlog.append('z')"
        ],
        "tags": [],
    },
    {"id": "h05", "args": ["log.append(__name__.upper())"], "tags": []},
    {"id": "h06", "args": ["x = 1\nif x:\n    log.append(x)"], "tags": []},
    {
        "id": "h07",
        "args": ["for i in range(3):\n    log.append(i)\nlog.append(len(log))"],
        "tags": [],
    },
    {
        "id": "h08",
        "args": ["def main():\n    log.append('main()')\n\nif __name__ == '__main__':\n    main()"],
        "tags": [],
    },
    {"id": "h09", "args": ["log.append(__name__ == 'mymod')"], "tags": []},
]


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return []  # no brute.py: the cross-check is skipped
