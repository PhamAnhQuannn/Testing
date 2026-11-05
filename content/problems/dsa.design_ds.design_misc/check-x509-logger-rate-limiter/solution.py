class Logger:
    def __init__(self):
        self._last = {}

    def should_print_message(self, timestamp, message):
        last = self._last.get(message)
        if last is not None and timestamp < last + 10:
            return False
        self._last[message] = timestamp
        return True
