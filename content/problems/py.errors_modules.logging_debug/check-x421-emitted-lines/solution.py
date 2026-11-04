import io
import logging


def emitted_lines(level, records):
    logger = logging.getLogger("x421")
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(getattr(logging, level))
    buf = io.StringIO()
    handler = logging.StreamHandler(buf)
    handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
    logger.addHandler(handler)
    for name, msg in records:
        logger.log(getattr(logging, name), msg)
    logger.handlers.clear()
    return buf.getvalue().splitlines()
