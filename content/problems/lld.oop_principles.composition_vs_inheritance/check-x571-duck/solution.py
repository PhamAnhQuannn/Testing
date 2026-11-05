class _Fly:
    def __init__(self, text):
        self._text = text

    def fly(self):
        return self._text


class _Quack:
    def __init__(self, text):
        self._text = text

    def quack(self):
        return self._text


_FLY = {"fly": "I fly", "noway": "I can't fly"}
_QUACK = {"quack": "Quack", "mute": "...", "squeak": "Squeak"}


class Duck:
    """Composition: the duck HAS a fly behaviour and a quack behaviour and delegates to them."""

    def __init__(self, fly, quack):
        self._fly = _Fly(_FLY[fly])
        self._quack = _Quack(_QUACK[quack])

    def perform_fly(self):
        return self._fly.fly()

    def perform_quack(self):
        return self._quack.quack()

    def set_fly(self, name):
        self._fly = _Fly(_FLY[name])
