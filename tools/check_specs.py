"""Hand-written test INPUTS for tools/convert_checks.py (never `expected` values).

`assessment.json` gives each `write_code` item a `driver` that calls the reference a few times.
The converter records those calls (the first becomes the sample test, the rest hidden tests) and
adds the inputs below as more hidden tests, so every check problem has at least 5 hidden tests.
The first input of every list is an edge case (the converter tags it `edge`). Expected values are
always recorded from the reference solution by tools/gen_hidden.py.

Inputs must respect each prompt's preconditions (sorted array, exactly one answer, ...), because
a correct learner solution may differ from the reference where the prompt promises nothing.

`SPECIAL` holds the items whose driver cannot be replayed from JSON (linked lists, trees, classes,
callbacks) and so need an explicit entry point and explicit calls.
"""

# item id -> list of argument lists
EXTRA_INPUTS: dict[str, list[list]] = {
    "Q006": [[7], [10], [99999], [1000000007], [505]],
    "Q008": [[1], [0], [3], [30], [16]],
    "Q010": [[""], ["bcdfg"], ["Programming Language"], ["queueing"], ["AeIoU xyz"]],
    "Q012": [["a"], ["0P"], ["ab_a"], ["Was it a car or a cat I saw?"], ["No 'x' in Nixon"]],
    "Q013": [["aaaaaaaaaaaa"], ["abc"], ["abbbbbbbbbbbc"], ["zzzzyyx"], ["aabbbbcd"]],
    "Q019": [[[]], [[0, 0, 0]], [[5, 0, 0, 6, 0, 7]], [[1, 0]], [[0, 0, 1]]],
    "Q023": [
        [[1, 5], 6],
        [[-3, 4, 3, 90], 0],
        [[0, 4, 3, 0], 0],
        [[5, 75, 25], 100],
        [[1, 2, 3, 4, 5, 6], 11],
    ],
    "Q024": [["z"], ["aabbcc"], ["abcabcd"], ["dddccdbba"], [""]],
    "Q026": [[[[1]]], [[[], []]], [[[1], [2], [3]]], [[[5, 6, 7]]], [[[1, 2], [], [3, 4, 5], [6]]]],
    "Q028": [
        [["a"], 1],
        [["x", "y", "x", "y", "z"], 2],
        [["b", "a", "c"], 3],
        [["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4],
        [["a", "b", "a"], 2],
    ],
    "Q032": [
        [[7, 7, 7], 2],
        [[1, 2], 2],
        [[9, 8, 7, 6, 5], 5],
        [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4],
        [[-1, -2, -3], 1],
    ],
    "Q034": [[0], [1], [10], [50], [90]],
    "Q038": [
        [[]],
        [["b"]],
        [["bb", "a", "ccc", "aa", "c"]],
        [["zz", "y", "xx", "w"]],
        [["same", "same"]],
    ],
    "Q047": [
        [[], []],
        [[1, 2, 3], []],
        [[1, 3, 5, 7], [2, 4, 6, 8]],
        [[5, 6], [1, 2]],
        [[-3, 0, 2], [-1, 0, 9]],
    ],
    "Q051": [
        [[1], 0],
        [[1, 2, 3], 3],
        [[1, 2, 3, 4], 1],
        [[-1, -100, 3, 99], 2],
        [[1, 2, 3, 4, 5], 0],
    ],
    "Q052": [[[1]], [[-1, -2, -3]], [[1, 2, 3]], [[-2, -1]], [[8, -19, 5, -4, 20]]],
    "Q054": [
        [[]],
        [["a"]],
        [["ab", "ba", "abc", "cab", "bca"]],
        [["x", "y", "x"]],
        [["listen", "silent", "enlist", "google", "gogole"]],
    ],
    "Q055": [
        [[5]],
        [[1, 2, 0, 1]],
        [[9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]],
        [[10, 30, 20]],
        [[1, 1]],
    ],
    "Q056": [
        [[], 1],
        [[1], 5],
        [[99, 99], 1],
        [[1, 2, 1], 1],
        [[1, 2, 3, 4, 1], 4],
        [[4, 5, 4, 5], 1],
    ],
    "Q057": [
        ["", ""],
        ["ab", "aa"],
        ["paper", "title"],
        ["ab", "ca"],
        ["a", "a"],
        ["abca", "zbxz"],
    ],
    "Q059": [["1", "1"], ["1111", "1"], ["0", "1101"], ["1010", "10"], ["101010", "11011"]],
    "Q061": [
        [[5], [[0, 0]]],
        [[1, 2, 3, 4], [[0, 3], [1, 2], [2, 2]]],
        [[-1, -1, -1], [[0, 1], [1, 2]]],
        [[10, -10, 10], [[0, 2]]],
        [[0, 0, 0], [[0, 2], [1, 1]]],
    ],
    "Q062": [[[]], [[0]], [[1, -1, 1, -1]], [[3, -3, 3]], [[5, 5, -10, 0]]],
    "Q064": [["a"], ["aa"], ["abcba"], ["abab"], ["zzzz"]],
    "Q065": [["", "a"], ["aa", "a"], ["abcabc", "cab"], ["baa", "aa"], ["xyz", "xyz"]],
    "Q067": [[[]], [[2, 2, 2]], [[1, 0]], [[1, 2, 0, 1, 2, 0]], [[0, 1, 2, 0, 1, 2, 0]]],
    "Q068": [[[1]], [[7, 7, 7]], [[1, 1, 2]], [[5, 1, 5, 2, 5]], [[9, 9, 8, 8, 9]]],
    "Q070": [
        [[1, 2], 3],
        [[1, 2, 3, 4, 4, 9, 56, 90], 8],
        [[0, 0, 3, 4], 0],
        [[-5, -3, 1, 2], -3],
        [[2, 3, 4], 6],
        [[1, 3, 5], 100],
    ],
    "Q071": [
        [[]],
        [[0, 0, 0, 0]],
        [[-2, 0, 1, 1, 2]],
        [[-1, -1, -1, 2, 2]],
        [[3, -1, -2, 0, 1, 2]],
    ],
    "Q084": [[""], ["abc"], ["abccba"], ["aaa"], ["mississippi"]],
    "Q085": [[[]], [[50]], [[1, 2, 3]], [[3, 2, 1]], [[70, 71, 69, 75, 60]]],
    "Q086": [
        [["5"]],
        [["3", "4", "-"]],
        [["6", "3", "/"]],
        [["-7", "2", "/"]],
        [["2", "3", "4", "*", "+"]],
    ],
    "Q087": [[""], ["abc"], ["2[a]"], ["10[x]"], ["2[a3[b]]c"]],
    "Q093": [[1], [3], [10], [20], [40]],
    "Q094": [[3, 1], [3, 4], [5, 10], [10, 300], [30, 1048576]],
    "Q095": [
        [[1], 1],
        [[1], 0],
        [[2, 4, 6, 8], 8],
        [[1, 3, 5, 6], 0],
        [[1, 3, 5, 6, 9, 10], 10],
    ],
    "Q097": [[4], [15], [16], [99], [1000000]],
    "Q101": [
        [[1]],
        [[3, 2, 1]],
        [[1, 2, 3]],
        [[9, -1, 5, 0, -7, 5]],
        [[4, 3, 2, 1, 0, -1, -2, -3]],
    ],
    "Q102": [
        [[[1, 2]]],
        [[[1, 2], [2, 3]]],
        [[[1, 5], [2, 3]]],
        [[[10, 20], [1, 5], [5, 10]]],
        [[[1, 4], [3, 6]]],
    ],
    "Q103": [[[1]], [[0]], [[20, 1]], [[121, 12]], [[432, 43243]]],
    "Q258": [
        [["b", "b"]],
        [["a", "b"]],
        [["cat", "dog", "cat", "dog", "ant"]],
        [["q", "w", "e", "w", "q"]],
    ],
    "W185": [["hello"], ["a b"], ["  hello world  "], ["one two  three"], [""]],
    "W188": [["a", "b"], ["aab", "aba"], ["ab", "abc"], ["listen", "silent"], ["aacc", "ccac"]],
    "W189": [
        [[5], 10],
        [[2, 2, 2, 2], 4],
        [[1, 5, 7, -1, 5], 6],
        [[3, 3], 6],
        [[0, 0, 0], 0],
    ],
    "W190": [
        [[1]],
        [[0, 0, 0]],
        [[1, 1, 0, 0, 1]],
        [[0, 1, 1, 0, 1, 1, 1, 0]],
        [[1, 0, 1, 0, 1, 0, 0]],
    ],
    "W191": [
        [[]],
        [["abc", "abc"]],
        [["ab", "a", ""]],
        [["interview", "internet", "interval"]],
        [["x", "y"]],
    ],
    "W192": [[[9]], [[1, 9, 9]], [[4, 3, 2, 1]], [[9, 9, 9, 9]], [[0, 0, 9]]],
    "W193": [[[0, 0]], [[4, 3, 2, 1, 4]], [[1, 2, 1]], [[2, 3, 4, 5, 18, 17, 6]], [[5, 5, 5, 5]]],
    "W194": [[[]], [[1]], [[1, 1, 1]], [[1, 2, 3]], [[1, 1, 2, 2, 3, 3]], [[-1, -1, 0, 0, 5]]],
    "W198": [["", ""], ["#", "a#"], ["abc", "abd"], ["xy##z", "z"], ["bxj##tw", "bxo#j##tw"]],
    "W202": [[1], [3], [81], [-3], [243], [100]],
    # Wave 2 Round 6: DSA breadth (matrix, sliding window). First input of each is the edge case.
    "Q073": [
        [[5], 1],
        [[1, 1, 1, 1], 2],
        [[-5, -2, -10, -3], 2],
        [[0, 4, 0, 3, 2], 3],
        [[100, 200, 300], 3],
    ],
    "Q074": [[""], ["a"], ["abba"], ["dvdf"], ["tmmzuxt"]],
    "Q075": [
        [100, [1, 1, 1]],
        [7, [2, 3, 1, 2, 4, 3]],
        [4, [1, 4, 4]],
        [15, [1, 2, 3, 4, 5]],
        [6, [10]],
    ],
    "W204": [["BBB", 0], ["AAAA", 2], ["ABCDE", 1], ["ABBB", 1], ["XYZXYZ", 2], ["AABB", 1]],
    "Q137": [
        [[[1]]],
        [[[1, 2], [3, 4]]],
        [[[1, 2, 3], [4, 5, 6]]],
        [[[1], [2], [3]]],
        [[[1, 2, 3, 4]]],
    ],
    "Q138": [
        [[[1, 2], [3, 4]]],
        [[[0, 0], [0, 1]]],
        [[[2, 3, 4], [5, 6, 7], [8, 9, 10]]],
        [[[9, 8], [7, 6]]],
        [[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]],
        [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]],
    ],
    "W211": [
        [[[0]]],
        [[[1, 2, 3], [4, 5, 6]]],
        [[[1, 0], [0, 1]]],
        [[[1, 1], [1, 1]]],
        [[[0, 2], [3, 4]]],
        [[[5, 6, 7], [8, 0, 9], [1, 2, 3]]],
    ],
    # Wave 2 Round 7: heap + binary search variants. First input of each is the edge case.
    "Q107": [[[1, 1]], [[10]], [[2, 2, 2]], [[1, 3, 5, 7]], [[9, 8, 7, 6, 5]], [[100, 100, 50]]],
    "Q108": [
        [["a"], 1],
        [["a", "b", "c"], 2],
        [["z", "z", "a", "a", "m"], 2],
        [["x", "y", "x", "y", "z"], 3],
        [["apple", "app", "apple"], 1],
        [["b", "a", "b", "a", "c"], 2],
    ],
    "W201": [
        [[5], 1, 5],
        [[1, 2, 3], 1, 2],
        [[1, 2, 3, 4, 5], 2, 10],
        [[-5, -3, 0, 2, 8], 3, 1],
        [[1, 2, 3, 4], 4, 0],
        [[0, 1, 2, 3, 4, 5, 6], 3, 3],
    ],
    "Q109": [
        [[[1, 2], [3, 4]], 1],
        [[[1, 2], [3, 4]], 4],
        [[[1, 3, 5], [2, 4, 6], [7, 8, 9]], 5],
        [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 6],
        [[[-10, -5], [-3, 0]], 3],
        [[[2, 2], [2, 2]], 3],
    ],
    "Q098": [
        [[], 5],
        [[1], 1],
        [[1, 1, 1, 1], 1],
        [[1, 2, 3, 4, 5], 3],
        [[2, 2, 3, 3, 3, 4], 3],
        [[1, 2, 3], 7],
    ],
    "Q099": [
        [[1], 5],
        [[3, 1], 1],
        [[5, 1, 2, 3, 4], 5],
        [[4, 5, 6, 7, 0, 1, 2], 7],
        [[6, 7, 8, 1, 2, 3, 4, 5], 8],
        [[1, 2, 3, 4, 5], 3],
    ],
    # Wave 2 Round 9: graphs module. Args are plain JSON (ints, edge/adjacency lists, int grids);
    # first input of each is the edge case, all distinct from the driver's own calls.
    "Q148": [
        [2, []],
        [4, [[1, 3], [2, 3], [4, 3]]],
        [3, [[1, 2], [2, 3], [3, 1]]],
        [2, [[2, 1]]],
        [4, [[1, 2], [2, 3], [3, 4]]],
        [5, [[1, 5], [2, 5], [3, 5], [4, 5]]],
    ],
    "W213": [
        [1, [], 0, 0],
        [2, [[0, 1]], 0, 1],
        [4, [[0, 1], [1, 2], [2, 3]], 0, 3],
        [5, [[0, 1], [2, 3], [3, 4]], 0, 4],
        [6, [[0, 1], [1, 2], [3, 4], [4, 5]], 2, 5],
        [3, [[0, 1], [1, 2]], 2, 0],
    ],
    "Q149": [
        [1, []],
        [6, []],
        [5, [[0, 1], [2, 3], [1, 4]]],
        [4, [[0, 1], [1, 2], [2, 3], [3, 0]]],
        [7, [[0, 1], [2, 3], [4, 5]]],
        [2, [[0, 1]]],
    ],
    "Q150": [
        [[[]]],
        [[[], []]],
        [[[1], [0]]],
        [[[1, 2], [0, 2], [0, 1]]],
        [[[1], [0, 2], [1, 3], [2]]],
        [[[1, 2], [0], [0]]],
    ],
    "Q151": [
        [[[0]], 0, 0, 0],
        [[[1]], 0, 0, 5],
        [[[1, 1], [1, 1]], 0, 0, 2],
        [[[0, 0, 0], [0, 1, 0], [0, 0, 0]], 1, 1, 7],
        [[[1, 2], [2, 1]], 0, 0, 3],
        [[[5, 5], [5, 5]], 1, 1, 5],
    ],
    "Q152": [
        [[[0]]],
        [[[1]]],
        [[[1, 1, 1], [1, 1, 1]]],
        [[[1, 0, 1], [0, 0, 0], [1, 0, 1]]],
        [[[0, 0, 1, 0], [1, 1, 1, 0], [0, 1, 0, 0]]],
        [[[1, 1], [0, 0], [1, 1]]],
    ],
    "W214": [
        [[[1, 1]]],
        [[[1], [1]]],
        [[[1, 1], [1, 1]]],
        [[[0, 1, 0], [1, 1, 1], [0, 1, 0]]],
        [[[1, 1, 1]]],
        [[[1, 0], [1, 1]]],
    ],
    "Q153": [
        [2, [], 0, 0],
        [2, [[0, 1]], 0, 1],
        [4, [[0, 1], [1, 2], [2, 3]], 0, 3],
        [5, [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4]], 0, 4],
        [3, [[0, 1]], 0, 2],
        [6, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [0, 5]], 0, 5],
    ],
    "Q154": [
        [[[0]]],
        [[[2]]],
        [[[2, 1]]],
        [[[1]]],
        [[[2, 1, 1, 1, 1]]],
        [[[2, 0, 1]]],
    ],
    "W215": [
        [[[1]]],
        [[[0, 0]]],
        [[[0], [0]]],
        [[[0, 0], [0, 0]]],
        [[[0, 1, 0], [0, 1, 0], [0, 0, 0]]],
        [[[0, 0, 0], [1, 1, 1], [0, 0, 0]]],
    ],
    "Q155": [
        [1, []],
        [4, []],
        [3, [[0, 1], [1, 2]]],
        [3, [[0, 1], [1, 2], [2, 0]]],
        [4, [[1, 0], [2, 1], [3, 2]]],
        [5, [[1, 0], [2, 1], [0, 2]]],
    ],
    # Wave 2 Round 12: backtracking_core. References already return canonical-sorted lists, so plain
    # JSON inputs replay fine; first input is the edge case, all distinct from the driver's calls.
    "Q119": [
        [[]],
        [[1]],
        [[1, 2]],
        [[5, 7, 9]],
        [[1, 2, 3, 4]],
        [[2, 4, 6, 8, 10]],
    ],
    "Q120": [
        [0],
        [1],
        [2],
        [5],
        [6],
        [7],
    ],
    "W205": [
        [[]],
        [[1]],
        [[1, 2]],
        [[3, 5, 7]],
        [[9, 8, 7, 6, 5]],
        [[2, 4, 6, 8]],
    ],
    # Wave 2 Round 13: greedy_intervals. Interval/point inputs are plain JSON (int and
    # list[list[int]]); first input is the edge case, all distinct from the driver's own calls.
    "Q132": [
        [[1, 3]],
        [[0, 2, 4, 6]],
        [[-3, -2, -1]],
        [[10, 11, 12, 13, 14]],
        [[1]],
        [[2, 3, 5, 6, 8]],
    ],
    "Q133": [
        [[], [2, 3]],
        [[[1, 5]], [2, 3]],
        [[[1, 2], [5, 6]], [3, 4]],
        [[[1, 10]], [2, 3]],
        [[[1, 2], [4, 5], [7, 8]], [3, 6]],
        [[[3, 5]], [1, 2]],
    ],
    "W210": [
        [[[1, 2]]],
        [[[1, 2], [3, 4]]],
        [[[1, 5], [2, 3], [4, 6]]],
        [[[1, 10], [2, 3], [4, 5]]],
        [[[0, 1], [0, 2], [0, 3]]],
        [[[1, 100], [2, 3], [3, 4], [5, 6]]],
    ],
    "Q134": [
        [[[1, 2]]],
        [[[1, 10], [2, 3], [4, 5]]],
        [[[1, 2], [3, 4], [5, 6], [7, 8]]],
        [[[1, 100]]],
        [[[1, 5], [2, 6], [3, 7]]],
        [[[2, 3], [2, 3], [2, 3]]],
    ],
    "Q135": [
        [[[1, 0, 1]], 1],
        [[[2, 1, 5]], 2],
        [[[3, 2, 6], [2, 6, 9]], 4],
        [[[1, 1, 2], [1, 2, 3]], 1],
        [[[5, 0, 10]], 5],
        [[[2, 1, 3], [3, 3, 5]], 4],
    ],
    # Wave 2 Round 15: bit_basics. popcount (int), single_number (list[int], every value twice
    # except one), max_unique_len (list[str]); first input is the edge, distinct from driver calls.
    "Q158": [
        [1],
        [3],
        [255],
        [1023],
        [65536],
        [4095],
    ],
    "Q159": [
        [[5]],
        [[3, 3, 9]],
        [[1, 2, 2, 1, 8]],
        [[-4, -4, -7]],
        [[10, 20, 10]],
        [[0, 0, 5]],
    ],
    "Q260": [
        [[]],
        [["a"]],
        [["ab", "cd"]],
        [["abc", "abc"]],
        [["a", "b", "c", "d"]],
        [["xy", "yz", "zx"]],
    ],
}


def step(op: str, *args) -> tuple[str, list]:
    return op, list(args)


def sequence(cls: str, *steps: tuple[str, list]) -> dict:
    """A class_ops test: construct `cls()`, then call each (operation, arguments) in turn."""
    return {"ops": [cls, *(op for op, _ in steps)], "args": [[], *(args for _, args in steps)]}


def flags(n: int, bad: int) -> list[bool]:
    """`is_bad` as data: versions 1..n, every version from `bad` on is bad."""
    return [version >= bad for version in range(1, n + 1)]


def stack_tests() -> tuple[list[dict], list[dict]]:
    calls = [
        sequence(
            "Stack",
            step("push", 1),
            step("push", 2),
            step("pop"),
            step("peek"),
            step("is_empty"),
        )
    ]
    extras = [
        sequence("Stack", step("is_empty")),
        sequence(
            "Stack", step("push", 5), step("is_empty"), step("peek"), step("pop"), step("is_empty")
        ),
        sequence(
            "Stack",
            step("push", "a"),
            step("push", "b"),
            step("push", "c"),
            step("pop"),
            step("pop"),
            step("peek"),
        ),
        sequence(
            "Stack",
            step("push", 1),
            step("pop"),
            step("push", 2),
            step("peek"),
            step("pop"),
            step("is_empty"),
        ),
        sequence(
            "Stack",
            step("push", 1),
            step("push", 2),
            step("push", 3),
            step("push", 4),
            step("peek"),
            step("pop"),
            step("peek"),
            step("is_empty"),
        ),
        sequence("Stack", step("push", 0), step("peek"), step("is_empty")),
    ]
    return calls, extras


def queue_tests() -> tuple[list[dict], list[dict]]:
    calls = [
        sequence(
            "MyQueue",
            step("push", 1),
            step("push", 2),
            step("peek"),
            step("pop"),
            step("empty"),
            step("pop"),
            step("empty"),
        )
    ]
    extras = [
        sequence("MyQueue", step("empty")),
        sequence(
            "MyQueue", step("push", 7), step("empty"), step("peek"), step("pop"), step("empty")
        ),
        sequence(
            "MyQueue",
            step("push", 1),
            step("push", 2),
            step("push", 3),
            step("pop"),
            step("push", 4),
            step("pop"),
            step("pop"),
            step("pop"),
            step("empty"),
        ),
        sequence(
            "MyQueue",
            step("push", 1),
            step("peek"),
            step("push", 2),
            step("peek"),
            step("pop"),
            step("peek"),
        ),
        sequence(
            "MyQueue",
            step("push", 5),
            step("push", 6),
            step("pop"),
            step("push", 7),
            step("pop"),
            step("peek"),
        ),
    ]
    return calls, extras


def hashmap_tests() -> tuple[list[dict], list[dict]]:
    calls = [
        sequence(
            "MyHashMap",
            step("put", 1, 1),
            step("put", 98, 2),
            step("put", 1, 3),
            step("get", 1),
            step("get", 98),
            step("get", 2),
            step("remove", 1),
            step("get", 1),
            step("get", 98),
        )
    ]
    extras = [
        sequence("MyHashMap", step("get", 5)),
        sequence(
            "MyHashMap", step("put", 0, 10), step("get", 0), step("remove", 0), step("get", 0)
        ),
        # 2 and 99 collide (both 2 mod 97): chaining must still separate them.
        sequence(
            "MyHashMap", step("put", 2, 1), step("put", 99, 2), step("get", 2), step("get", 99)
        ),
        sequence("MyHashMap", step("remove", 7), step("get", 7)),
        sequence(
            "MyHashMap",
            step("put", 1, 1),
            step("put", 2, 2),
            step("put", 3, 3),
            step("put", 2, 22),
            step("get", 2),
            step("get", 1),
        ),
        sequence(
            "MyHashMap",
            step("put", 100, 5),
            step("get", 100),
            step("remove", 100),
            step("get", 100),
        ),
    ]
    return calls, extras


def timemap_tests() -> tuple[list[dict], list[dict]]:
    calls = [
        sequence(
            "TimeMap",
            step("set", "foo", "bar", 1),
            step("set", "foo", "bar2", 4),
            step("get", "foo", 1),
            step("get", "foo", 3),
            step("get", "foo", 4),
            step("get", "foo", 0),
            step("get", "x", 5),
        )
    ]
    extras = [
        sequence("TimeMap", step("get", "missing", 10)),
        sequence(
            "TimeMap",
            step("set", "k", "v", 5),
            step("get", "k", 5),
            step("get", "k", 4),
            step("get", "k", 6),
        ),
        sequence(
            "TimeMap",
            step("set", "a", "1", 1),
            step("set", "a", "2", 2),
            step("set", "a", "3", 3),
            step("get", "a", 2),
            step("get", "a", 1),
        ),
        sequence("TimeMap", step("set", "x", "first", 10), step("get", "x", 10)),
        sequence(
            "TimeMap", step("set", "p", "q", 100), step("get", "p", 50), step("get", "p", 150)
        ),
        sequence(
            "TimeMap",
            step("set", "m", "1", 1),
            step("set", "n", "2", 2),
            step("get", "m", 5),
            step("get", "n", 5),
        ),
    ]
    return calls, extras


def minstack_tests() -> tuple[list[dict], list[dict]]:
    calls = [
        sequence(
            "MinStack",
            step("push", -2),
            step("push", 0),
            step("push", -3),
            step("get_min"),
            step("pop"),
            step("top"),
            step("get_min"),
        )
    ]
    extras = [
        sequence("MinStack", step("push", 1), step("top"), step("get_min")),
        sequence(
            "MinStack",
            step("push", 5),
            step("push", 5),
            step("push", 5),
            step("get_min"),
            step("pop"),
            step("get_min"),
        ),
        sequence(
            "MinStack",
            step("push", 3),
            step("push", 2),
            step("push", 1),
            step("get_min"),
            step("pop"),
            step("pop"),
            step("get_min"),
        ),
        sequence("MinStack", step("push", 1), step("push", 2), step("push", 3), step("get_min")),
        sequence(
            "MinStack",
            step("push", -1),
            step("push", -2),
            step("pop"),
            step("top"),
            step("get_min"),
        ),
        sequence(
            "MinStack",
            step("push", 0),
            step("push", -1),
            step("push", 0),
            step("get_min"),
            step("pop"),
            step("get_min"),
        ),
    ]
    return calls, extras


def underground_tests() -> tuple[list[dict], list[dict]]:
    calls = [
        sequence(
            "Underground",
            step("check_in", 45, "A", 3),
            step("check_in", 32, "A", 8),
            step("check_out", 45, "B", 15),
            step("check_out", 32, "B", 22),
            step("average", "A", "B"),
            step("check_in", 10, "A", 24),
            step("check_out", 10, "B", 38),
            step("average", "A", "B"),
        )
    ]
    extras = [
        sequence(
            "Underground",
            step("check_in", 1, "X", 0),
            step("check_out", 1, "Y", 10),
            step("average", "X", "Y"),
        ),
        sequence(
            "Underground",
            step("check_in", 1, "A", 0),
            step("check_out", 1, "B", 4),
            step("check_in", 2, "A", 10),
            step("check_out", 2, "B", 20),
            step("average", "A", "B"),
        ),
        sequence(
            "Underground",
            step("check_in", 5, "P", 5),
            step("check_out", 5, "Q", 9),
            step("average", "P", "Q"),
        ),
        sequence(
            "Underground",
            step("check_in", 1, "A", 0),
            step("check_in", 2, "C", 0),
            step("check_out", 1, "B", 5),
            step("check_out", 2, "D", 10),
            step("average", "A", "B"),
            step("average", "C", "D"),
        ),
        sequence(
            "Underground",
            step("check_in", 7, "M", 2),
            step("check_out", 7, "N", 8),
            step("check_in", 7, "M", 10),
            step("check_out", 7, "N", 14),
            step("average", "M", "N"),
        ),
    ]
    return calls, extras


def ttlcache_tests() -> tuple[list[dict], list[dict]]:
    """TTLCache's constructor takes the ttl, so the first args entry is [ttl] (not [])."""

    def seq(ttl: int, *steps: tuple[str, list]) -> dict:
        return {
            "ops": ["TTLCache", *(op for op, _ in steps)],
            "args": [[ttl], *(a for _, a in steps)],
        }

    calls = [
        seq(
            5, step("put", "a", 1, 0), step("get", "a", 4), step("get", "a", 5), step("get", "a", 6)
        )
    ]
    extras = [
        seq(5, step("get", "x", 0)),
        seq(3, step("put", "k", 9, 0), step("get", "k", 2), step("get", "k", 3)),
        seq(10, step("put", "a", 1, 0), step("put", "a", 2, 5), step("get", "a", 9)),
        seq(1, step("put", "p", 7, 100), step("get", "p", 100), step("get", "p", 101)),
        seq(100, step("put", "m", 1, 0), step("get", "m", 50)),
        seq(
            5,
            step("put", "a", 1, 0),
            step("put", "b", 2, 1),
            step("get", "a", 4),
            step("get", "b", 4),
        ),
    ]
    return calls, extras


# Items whose driver cannot be replayed from JSON. Keys:
#   mode     function (default) | class_ops
#   target   function name (function) or class name (class_ops)
#   keep     top-level names of the reference that go into solution.py (helpers are dropped)
#   params   [(name, type)] where it cannot be inferred (list_node / tree_node / bool lists)
#   returns  return type when it is list_node / tree_node
#   calls    the driver's calls as argument lists (or class_ops sequences); first one = sample
#   extras   more hidden inputs; the first is an edge case
#   solution replacement reference code (only where the item must change shape, see `note`)
#   note     extra Vietnamese sentence appended to the statement
SPECIAL: dict[str, dict] = {
    "Q079": {
        "target": "reverse_list",
        "keep": ["reverse_list"],
        "params": [("head", "list_node")],
        "returns": "list_node",
        "calls": [[[1, 2, 3, 4]], [[]], [[7]]],
        "extras": [[[1, 2]], [[5, 4, 3, 2, 1]], [[1, 1, 1]], [[10, 20, 30]], [[9, 8]]],
    },
    "Q080": {
        "target": "middle",
        "keep": ["middle"],
        "params": [("head", "list_node")],
        "returns": "list_node",
        "calls": [[[1, 2, 3, 4, 5]], [[1, 2, 3, 4]]],
        "extras": [[[1]], [[1, 2]], [[1, 2, 3]], [[9, 8, 7, 6, 5, 4]], [[0, 0, 0, 0, 0]]],
        "note": (
            "Bản chấm tự động chỉ kiểm tra `middle(head)`: hàm trả nút giữa, kết quả được "
            "so sánh bằng danh sách giá trị từ nút giữa đến hết. Phần `has_cycle` cần danh sách "
            "có vòng nên không biểu diễn được bằng dữ liệu test."
        ),
    },
    "Q081": {
        "target": "remove_nth_from_end",
        "keep": ["remove_nth_from_end"],
        "params": [("head", "list_node"), ("n", "int")],
        "returns": "list_node",
        "calls": [[[1, 2, 3, 4, 5], 2], [[1], 1], [[1, 2], 2]],
        "extras": [
            [[1, 2], 1],
            [[1, 2, 3], 3],
            [[1, 2, 3, 4], 4],
            [[5, 6, 7, 8, 9], 5],
            [[1, 2, 3], 2],
        ],
    },
    "Q105": {
        "target": "max_depth",
        "keep": ["max_depth"],
        "params": [("root", "tree_node")],
        "returns": "int",
        "calls": [[[3, 9, 20, None, None, 15, 7]], [[]]],
        "extras": [
            [[1]],
            [[1, 2]],
            [[1, None, 2, None, 3]],
            [[1, 2, 3, 4, 5, None, None, 6]],
            [[2, 1, 3]],
        ],
        "note": (
            "Bản chấm tự động chỉ kiểm tra `max_depth(root)`; `inorder(root)` không nằm trong "
            "bộ test (mỗi bài chỉ có một hàm vào)."
        ),
    },
    "W195": {
        "target": "merge_two",
        "keep": ["merge_two"],
        "params": [("a", "list_node"), ("b", "list_node")],
        "returns": "list_node",
        "calls": [[[1, 2, 4], [1, 3, 4]], [[], [0]]],
        "extras": [[[], []], [[1], []], [[5, 6], [1, 2]], [[1, 2, 3], [4, 5, 6]], [[2, 2], [2, 2]]],
    },
    "W196": {
        "target": "is_pal_list",
        "keep": ["is_pal_list"],
        "params": [("head", "list_node")],
        "returns": "bool",
        "calls": [[[1, 2, 2, 1]], [[1, 2]], [[1, 2, 1]]],
        "extras": [[[1]], [[]], [[1, 1]], [[1, 2, 3, 2, 1]], [[1, 2, 3, 4]], [[1, 0, 0, 1, 0]]],
    },
    "W203": {
        "target": "invert",
        "keep": ["invert"],
        "params": [("root", "tree_node")],
        "returns": "tree_node",
        "calls": [[[4, 2, 7, 1, 3, 6, 9]], [[]]],
        "extras": [
            [[1]],
            [[1, 2]],
            [[1, None, 2]],
            [[1, 2, 3, 4, 5]],
            [[5, 3, 8, 2, 4, 7, 9]],
        ],
    },
    # Wave 2 Round 8: trees module (drivers build trees via tree(vals), cannot be JSON-replayed).
    "Q121": {
        "target": "has_path_sum",
        "keep": ["has_path_sum"],
        "params": [("root", "tree_node"), ("target", "int")],
        "calls": [
            [[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22],
            [[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 5],
            [[], 0],
        ],
        "extras": [[[], 1], [[1], 1], [[1], 2], [[1, 2], 3], [[1, 2, 3], 4]],
    },
    "Q122": {
        "target": "is_balanced",
        "keep": ["is_balanced"],
        "params": [("root", "tree_node")],
        "calls": [[[3, 9, 20, None, None, 15, 7]], [[1, 2, 2, 3, 3, None, None, 4, 4]], [[]]],
        "extras": [
            [[1]],
            [[1, 2]],
            [[1, 2, None, 3]],
            [[1, None, 2, None, 3]],
            [[1, 2, 3, 4, 5, 6, 7]],
        ],
    },
    "W206": {
        "target": "good_nodes",
        "keep": ["good_nodes"],
        "params": [("root", "tree_node")],
        "calls": [[[3, 1, 4, 3, None, 1, 5]], [[3, 3, None, 4, 2]], [[1]]],
        "extras": [[[1, 2, 3]], [[2, 4]], [[10, 5, 15]], [[1, 1, 1]], [[3, 2, 1]]],
    },
    # Q123/Q124/W207 references use collections.deque; keeping only the target drops the import,
    # so supply a self-contained (deque-free) solution that walks the tree level by level.
    "Q123": {
        "target": "level_order",
        "params": [("root", "tree_node")],
        "calls": [[[3, 9, 20, None, None, 15, 7]], [[]]],
        "extras": [
            [[1]],
            [[1, 2]],
            [[1, None, 2]],
            [[1, 2, 3, 4, 5, 6, 7]],
            [[5, 4, 8, 11, None, 13, 4]],
        ],
        "solution": (
            "def level_order(root):\n"
            "    if not root:\n"
            "        return []\n"
            "    out, level = [], [root]\n"
            "    while level:\n"
            "        out.append([n.val for n in level])\n"
            "        level = [c for n in level for c in (n.left, n.right) if c]\n"
            "    return out\n"
        ),
    },
    "Q124": {
        "target": "zigzag",
        "params": [("root", "tree_node")],
        "calls": [[[3, 9, 20, None, None, 15, 7]], [[1, 2, 3, 4, 5, 6, 7]]],
        "extras": [[[]], [[1]], [[1, 2]], [[1, None, 2]], [[1, 2, 3, 4, None, None, 7]]],
        "solution": (
            "def zigzag(root):\n"
            "    if not root:\n"
            "        return []\n"
            "    out, level, ltr = [], [root], True\n"
            "    while level:\n"
            "        vals = [n.val for n in level]\n"
            "        out.append(vals if ltr else vals[::-1])\n"
            "        ltr = not ltr\n"
            "        level = [c for n in level for c in (n.left, n.right) if c]\n"
            "    return out\n"
        ),
    },
    "W207": {
        "target": "avg_levels",
        "params": [("root", "tree_node")],
        "calls": [[[3, 9, 20, None, None, 15, 7]], [[]]],
        "extras": [
            [[1]],
            [[1, 2, 3]],
            [[4, 2, 8, 1, 3]],
            [[10, 20, None, 30]],
            [[2, 1, 3]],
        ],
        "solution": (
            "def avg_levels(root):\n"
            "    if not root:\n"
            "        return []\n"
            "    out, level = [], [root]\n"
            "    while level:\n"
            "        out.append(sum(n.val for n in level) / len(level))\n"
            "        level = [c for n in level for c in (n.left, n.right) if c]\n"
            "    return out\n"
        ),
    },
    "Q126": {
        "target": "is_valid_bst",
        "keep": ["is_valid_bst"],
        "params": [("root", "tree_node")],
        "calls": [[[2, 1, 3]], [[5, 1, 4, None, None, 3, 6]], [[5, 4, 6, None, None, 3, 7]]],
        "extras": [
            [[2, 2]],
            [[]],
            [[1]],
            [[10, 5, 15]],
            [[10, 5, 15, None, None, 6, 20]],
            [[3, 1, 5, 0, 2, 4, 6]],
        ],
    },
    "Q127": {
        "target": "kth_smallest",
        "keep": ["kth_smallest"],
        "params": [("root", "tree_node"), ("k", "int")],
        "calls": [[[3, 1, 4, None, 2], 1], [[5, 3, 6, 2, 4, None, None, 1], 3]],
        "extras": [
            [[1], 1],
            [[2, 1, 3], 2],
            [[2, 1, 3], 1],
            [[5, 3, 6, 2, 4], 4],
            [[4, 2, 6, 1, 3, 5, 7], 5],
        ],
    },
    "W208": {
        "target": "lca_bst",
        "keep": ["lca_bst"],
        "params": [("root", "tree_node"), ("p", "int"), ("q", "int")],
        "calls": [
            [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8],
            [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 4],
            [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 3, 5],
        ],
        "extras": [
            [[2, 1, 3], 1, 3],
            [[2, 1, 3], 1, 1],
            [[5, 3, 8, 1, 4], 1, 4],
            [[5, 3, 8, 1, 4], 3, 8],
            [[6, 2, 8, 0, 4, 7, 9], 7, 9],
        ],
    },
    # Wave 2 Round 9: topological order is not unique, so the driver checks validity instead of
    # printing find_order directly. Pin a canonical answer (Kahn + heap = lexicographically smallest
    # order, empty list on a cycle) so the check can compare exactly.
    "Q156": {
        "target": "find_order",
        "params": [("n", "int"), ("prereqs", "list[list[int]]")],
        "returns": "list",
        "solution": (
            "import heapq\n\n\n"
            "def find_order(n, prereqs):\n"
            "    indeg = [0] * n\n"
            "    adj = [[] for _ in range(n)]\n"
            "    for a, b in prereqs:\n"
            "        adj[b].append(a)\n"
            "        indeg[a] += 1\n"
            "    heap = [i for i in range(n) if indeg[i] == 0]\n"
            "    heapq.heapify(heap)\n"
            "    order = []\n"
            "    while heap:\n"
            "        node = heapq.heappop(heap)\n"
            "        order.append(node)\n"
            "        for nxt in adj[node]:\n"
            "            indeg[nxt] -= 1\n"
            "            if indeg[nxt] == 0:\n"
            "                heapq.heappush(heap, nxt)\n"
            "    return order if len(order) == n else []\n"
        ),
        "calls": [[4, [[1, 0], [2, 0], [3, 1], [3, 2]]], [2, [[0, 1], [1, 0]]]],
        "extras": [
            [1, []],
            [2, []],
            [3, [[0, 1], [0, 2]]],
            [4, [[1, 0], [2, 1], [3, 2]]],
            [3, [[0, 1], [1, 2], [2, 0]]],
            [5, [[1, 0], [2, 0], [3, 1], [4, 2]]],
        ],
        "note": (
            "LƯU Ý: khác với mô tả gốc ở trên, bản chấm tự động KHÔNG kiểm tra tính hợp lệ chung "
            "chung mà so khớp CHÍNH XÁC với thứ tự topo nhỏ nhất theo thứ tự từ điển (min-heap "
            "trong Kahn); nếu đồ thị có chu trình trả về danh sách rỗng."
        ),
    },
    "W199": {
        "target": "first_bad",
        "keep": ["first_bad"],
        "params": [("n", "int"), ("is_bad", "list[bool]")],
        "returns": "int",
        "solution": (
            "def first_bad(n, is_bad):\n"
            "    lo, hi = 1, n\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if is_bad[mid - 1]:\n"
            "            hi = mid\n"
            "        else:\n"
            "            lo = mid + 1\n"
            "    return lo\n"
        ),
        "calls": [[5, flags(5, 4)], [1, flags(1, 1)], [10, flags(10, 10)]],
        "extras": [
            [2, flags(2, 1)],
            [2, flags(2, 2)],
            [7, flags(7, 4)],
            [16, flags(16, 16)],
            [100, flags(100, 37)],
        ],
        "note": (
            "Trong bản chấm tự động, `is_bad` là list gồm `n` giá trị bool: `is_bad[v - 1]` cho "
            "biết phiên bản `v` có lỗi hay không (thay cho hàm gọi lại trong đề gốc)."
        ),
    },
    "Q077": {
        "mode": "class_ops",
        "target": "Stack",
        "keep": ["Stack"],
        "tests": stack_tests(),
        "note": "Bản chấm tự động không kiểm tra trường hợp `pop` khi rỗng ném `IndexError`.",
    },
    "Q083": {
        "mode": "class_ops",
        "target": "MyQueue",
        "keep": ["MyQueue"],
        "tests": queue_tests(),
    },
    # Wave 2 Round 14: design_ds. All five are classes whose driver is a method sequence, so they
    # run as class_ops with the upstream reference class kept as the solution.
    "Q128": {
        "mode": "class_ops",
        "target": "MyHashMap",
        "keep": ["MyHashMap"],
        "tests": hashmap_tests(),
    },
    "Q129": {
        "mode": "class_ops",
        "target": "TimeMap",
        "keep": ["TimeMap"],
        "tests": timemap_tests(),
    },
    "Q130": {
        "mode": "class_ops",
        "target": "MinStack",
        "keep": ["MinStack"],
        "tests": minstack_tests(),
    },
    "Q131": {
        "mode": "class_ops",
        "target": "Underground",
        "keep": ["Underground"],
        "tests": underground_tests(),
    },
    "W209": {
        "mode": "class_ops",
        "target": "TTLCache",
        "keep": ["TTLCache"],
        "tests": ttlcache_tests(),
    },
    # Wave 2 Round 15: W217 defines two functions (missing_number + is_pow2); the driver calls both,
    # so it is not plain-JSON replayable. Grade only missing_number; keep both in the solution.
    "W217": {
        "target": "missing_number",
        "keep": ["missing_number", "is_pow2"],
        "params": [("nums", "list[int]")],
        "calls": [[[3, 0, 1]], [[0, 1]]],
        "extras": [
            [[0]],
            [[1, 0]],
            [[0, 2, 3, 1]],
            [[2, 0, 1]],
            [[0, 1, 2, 3, 5, 4, 6]],
            [[4, 3, 2, 1, 0]],
        ],
        "note": "Bản chấm tự động chỉ kiểm tra `missing_number`; `is_pow2` không được chấm.",
    },
}
