def lookup_order(ops):
    log = []

    class D:
        def __get__(self, obj, owner=None):
            return "data"

        def __set__(self, obj, value):
            log.append("d=" + str(value))

    class N:
        def __get__(self, obj, owner=None):
            return "nondata"

    class C:
        d = D()
        n = N()

    c = C()
    for name, value in ops:
        setattr(c, name, value)
    return [c.d, c.n, log]
