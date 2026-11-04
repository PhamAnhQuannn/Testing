class Point:
    """Value class: equality and hash use the same fields."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))


def distinct_points(pairs):
    return len({Point(x, y) for x, y in pairs})
