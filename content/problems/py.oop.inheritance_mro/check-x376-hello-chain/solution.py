def hello_chain(order):
    """Build A, B(A), C(A) and D(bases per order); return D().hello()."""

    class A:
        def hello(self):
            return "A"

    class B(A):
        def hello(self):
            return "B>" + super().hello()

    class C(A):
        def hello(self):
            return "C>" + super().hello()

    picked = {"B": B, "C": C}
    bases = tuple(picked[ch] for ch in order) or (A,)
    D = type("D", bases, {})
    return D().hello()
