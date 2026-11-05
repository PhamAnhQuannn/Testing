class Library:
    """Core library API. Validation is reported through return values."""

    def __init__(self):
        # title -> [available, borrowed]; dict gives O(1) lookup by title
        self.books = {}

    def add_book(self, title, copies):
        entry = self.books.setdefault(title, [0, 0])
        entry[0] += copies

    def borrow(self, title):
        entry = self.books.get(title)
        if entry is None or entry[0] <= 0:
            return False
        entry[0] -= 1
        entry[1] += 1
        return True

    def return_book(self, title):
        entry = self.books.get(title)
        if entry is None or entry[1] <= 0:
            return False
        entry[0] += 1
        entry[1] -= 1
        return True

    def available(self, title):
        entry = self.books.get(title)
        return 0 if entry is None else entry[0]
