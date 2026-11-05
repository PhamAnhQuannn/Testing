class FileStore:
    def __init__(self):
        self._files = {}

    @staticmethod
    def _norm(path):
        return "/" + "/".join(p for p in path.split("/") if p)

    def add_file(self, path, size):
        self._files[self._norm(path)] = size

    def _under(self, dir_path):
        d = self._norm(dir_path)
        prefix = "/" if d == "/" else d + "/"
        return [(p, s) for p, s in self._files.items() if p.startswith(prefix)]

    def total_size(self, dir_path):
        return sum(s for _, s in self._under(dir_path))

    def find_by_min_size(self, dir_path, min_size):
        return sorted(p for p, s in self._under(dir_path) if s >= min_size)
