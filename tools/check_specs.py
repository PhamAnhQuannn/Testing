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
}
