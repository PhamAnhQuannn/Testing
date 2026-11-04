def add_vectors(a, b):
    """Add two [x, y] lists via a Vector class and return repr."""

    class Vector:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __add__(self, other):
            return Vector(self.x + other.x, self.y + other.y)

        def __repr__(self):
            return f"Vector({self.x}, {self.y})"

    return repr(Vector(*a) + Vector(*b))
