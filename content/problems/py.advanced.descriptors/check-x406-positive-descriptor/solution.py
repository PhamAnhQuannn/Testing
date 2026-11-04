def positive_demo(values):
    class Positive:
        def __set_name__(self, owner, name):
            self.name = name
            self.key = "_" + name

        def __get__(self, obj, owner=None):
            if obj is None:
                return self
            return obj.__dict__.get(self.key)

        def __set__(self, obj, value):
            if value <= 0:
                raise ValueError("must be positive")
            obj.__dict__[self.key] = value

    class Item:
        price = Positive()

    item = Item()
    outcomes = []
    for v in values:
        try:
            item.price = v
            outcomes.append("ok")
        except ValueError:
            outcomes.append("err")
    return [Item.__dict__["price"].name, outcomes, item.price]
