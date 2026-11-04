class Account:
    def __init__(self, name):
        self.name = name
        self._balance = 0
        self.ok = 0
        self.failed = 0

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0 or amount > self._balance:
            raise ValueError("invalid withdrawal")
        self._balance -= amount

    def apply(self, cmd, amount):
        try:
            getattr(self, cmd)(amount)
            self.ok += 1
        except ValueError:
            self.failed += 1


def bank_summary(ops):
    accounts = {}
    for name, cmd, amount in ops:
        acct = accounts.setdefault(name, Account(name))
        acct.apply(cmd, amount)
    return [
        [a.name, a.balance, a.ok, a.failed] for a in sorted(accounts.values(), key=lambda a: a.name)
    ]
