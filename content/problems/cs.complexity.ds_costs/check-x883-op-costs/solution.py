# Bảng chi phí cố định (structure, operation) -> Big-O.
COST = {
    ("array", "index"): "O(1)",
    ("array", "search"): "O(n)",
    ("array", "append"): "O(1)",
    ("array", "insert_front"): "O(n)",
    ("dict", "get"): "O(1)",
    ("dict", "set"): "O(1)",
    ("set", "contains"): "O(1)",
    ("list", "contains"): "O(n)",
    ("linked_list", "prepend"): "O(1)",
    ("linked_list", "index"): "O(n)",
    ("heap", "push"): "O(log n)",
    ("heap", "pop_min"): "O(log n)",
    ("heap", "peek"): "O(1)",
    ("bst", "search"): "O(log n)",
    ("sorted", "binary_search"): "O(log n)",
}


def op_costs(ops):
    return [COST.get((s, o), "O(?)") for s, o in ops]
