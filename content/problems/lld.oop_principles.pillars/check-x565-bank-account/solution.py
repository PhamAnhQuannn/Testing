class BankAccount:
    """Encapsulation: balance is private state, only changed through validated methods."""

    def __init__(self):
        self._balance = 0

    def deposit(self, n):
        if n > 0:
            self._balance += n

    def withdraw(self, n):
        if 0 < n <= self._balance:
            self._balance -= n

    def balance(self):
        return self._balance
