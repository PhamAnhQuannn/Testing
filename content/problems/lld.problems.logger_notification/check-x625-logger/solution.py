class Logger:
    """Level-filtered handlers kept in insertion order. DEBUG=0 < INFO=1 < ERROR=2."""

    LEVELS = {"DEBUG": 0, "INFO": 1, "ERROR": 2}

    def __init__(self):
        self.handlers = []  # list of (name, level_int) in insertion order

    def add_handler(self, name, level):
        self.handlers.append((name, self.LEVELS[level]))

    def log(self, level, msg):
        lv = self.LEVELS[level]
        return [name for name, thr in self.handlers if thr <= lv]

    def handler_count(self):
        return len(self.handlers)
