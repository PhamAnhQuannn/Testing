def bag_report(data, names):
    class Bag:
        def __init__(self, d):
            for key, value in d.items():
                setattr(self, key, value)

        def __getattr__(self, name):
            return name.upper()

    bag = Bag(data)
    return [sorted(vars(bag)), [getattr(bag, n) for n in names]]
