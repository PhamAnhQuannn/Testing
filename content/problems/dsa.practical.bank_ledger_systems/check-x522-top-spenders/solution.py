class Ledger:
    def __init__(self):
        self._spent = {}

    def open(self, account_id):
        if account_id not in self._spent:
            self._spent[account_id] = 0

    def pay(self, account_id, amount):
        if account_id in self._spent and amount > 0:
            self._spent[account_id] += amount

    def transfer(self, src, dst, amount):
        if src not in self._spent or dst not in self._spent or amount <= 0:
            return False
        self._spent[src] += amount
        return True

    def top_spenders(self, k):
        order = sorted(self._spent, key=lambda a: (-self._spent[a], a))
        return order[: max(k, 0)]
