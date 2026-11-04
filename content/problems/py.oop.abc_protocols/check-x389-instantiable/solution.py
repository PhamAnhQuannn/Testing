from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self):
        """Area."""

    @abstractmethod
    def perimeter(self):
        """Perimeter."""


def _zero(self):
    return 0


def instantiable(impls):
    out = []
    for names in impls:
        cls = type("Sub", (Shape,), {name: _zero for name in names})
        try:
            cls()
        except TypeError:
            out.append(False)
        else:
            out.append(True)
    return out
