class BrowserHistory:
    def __init__(self, homepage):
        self._pages = [homepage]
        self._i = 0

    def visit(self, url):
        del self._pages[self._i + 1 :]
        self._pages.append(url)
        self._i += 1

    def back(self, steps):
        self._i = max(0, self._i - steps)
        return self._pages[self._i]

    def forward(self, steps):
        self._i = min(len(self._pages) - 1, self._i + steps)
        return self._pages[self._i]
