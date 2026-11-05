class EmailFormatter:
    def format(self, text):
        return f"EMAIL: {text}"


class SmsFormatter:
    def format(self, text):
        return f"SMS: {text}"


class PushFormatter:
    def format(self, text):
        return f"PUSH: {text}"


class RawFormatter:
    def format(self, text):
        return f"RAW: {text}"


FACTORY = {"email": EmailFormatter, "sms": SmsFormatter, "push": PushFormatter}


def make_message(kind, text):
    return FACTORY.get(kind, RawFormatter)().format(text)
