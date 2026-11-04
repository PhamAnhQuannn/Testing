import io
import logging


def route(child_level, handler_level, records, propagate):
    parent = logging.getLogger("x422")
    child = logging.getLogger("x422.app")
    for lg in (parent, child):
        lg.handlers.clear()
    parent.propagate = False
    parent.setLevel(logging.DEBUG)
    child.propagate = propagate
    child.setLevel(getattr(logging, child_level))

    child_buf = io.StringIO()
    child_handler = logging.StreamHandler(child_buf)
    child_handler.setFormatter(logging.Formatter("C:%(levelname)s:%(message)s"))
    child.addHandler(child_handler)

    parent_buf = io.StringIO()
    parent_handler = logging.StreamHandler(parent_buf)
    parent_handler.setLevel(getattr(logging, handler_level))
    parent_handler.setFormatter(logging.Formatter("P:%(levelname)s:%(name)s:%(message)s"))
    parent.addHandler(parent_handler)

    for name, msg in records:
        child.log(getattr(logging, name), msg)
    for lg in (parent, child):
        lg.handlers.clear()
    return [child_buf.getvalue().splitlines(), parent_buf.getvalue().splitlines()]
