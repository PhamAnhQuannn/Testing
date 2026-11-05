class Bank:
    def __init__(self):
        self._bal = {}

    def open(self, account_id):
        if account_id not in self._bal:
            self._bal[account_id] = 0

    def deposit(self, account_id, amount):
        if account_id not in self._bal or amount <= 0:
            return False
        self._bal[account_id] += amount
        return True

    def withdraw(self, account_id, amount):
        if account_id not in self._bal or amount <= 0:
            return False
        if self._bal[account_id] < amount:
            return False
        self._bal[account_id] -= amount
        return True

    def transfer(self, src, dst, amount):
        if src not in self._bal or dst not in self._bal or amount <= 0:
            return False
        if self._bal[src] < amount:
            return False
        self._bal[src] -= amount
        self._bal[dst] += amount
        return True

    def balance(self, account_id):
        return self._bal.get(account_id)
