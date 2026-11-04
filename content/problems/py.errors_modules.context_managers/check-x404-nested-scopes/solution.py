from contextlib import ExitStack, contextmanager


@contextmanager
def scoped(log, name):
    """Log enter, then exit even on error."""
    log.append("enter " + name)
    try:
        yield name
    finally:
        log.append("exit " + name)


def nested(names, fail):
    log = []
    try:
        with ExitStack() as stack:
            for n in names:
                stack.enter_context(scoped(log, n))
            log.append("body")
            if fail:
                raise RuntimeError("x")
    except RuntimeError:
        log.append("caught")
    return log
