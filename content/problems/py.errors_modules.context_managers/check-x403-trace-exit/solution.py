class Tracer:
    """Log enter/exit; swallow only ValueError."""

    def __init__(self, log):
        self.log = log

    def __enter__(self):
        self.log.append("enter")
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.log.append("exit")
            return False
        self.log.append("exit:" + exc_type.__name__)
        return issubclass(exc_type, ValueError)


def run(kind):
    log = []
    try:
        with Tracer(log):
            log.append("body")
            if kind == "value":
                raise ValueError("v")
            if kind == "key":
                raise KeyError("k")
            log.append("end")
    except KeyError:
        log.append("caught:KeyError")
        return log
    log.append("after")
    return log
