from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self):
        """Return the area as an int."""


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side


class Rect(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h


class Tri(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return self.base * self.height // 2


KINDS = {"sq": Square, "rect": Rect, "tri": Tri}


def sorted_areas(specs):
    return sorted(KINDS[kind](*dims).area() for kind, *dims in specs)
