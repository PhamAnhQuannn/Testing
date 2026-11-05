class FileSystem:
    def __init__(self):
        self._root = {}

    @staticmethod
    def _parts(path):
        return [p for p in path.split("/") if p]

    def _walk(self, parts):
        node = self._root
        for p in parts:
            node = node[p]
        return node

    def ls(self, path):
        parts = self._parts(path)
        node = self._walk(parts)
        if isinstance(node, str):
            return [parts[-1]]
        return sorted(node)

    def mkdir(self, path):
        node = self._root
        for p in self._parts(path):
            node = node.setdefault(p, {})

    def add_content_to_file(self, path, content):
        parts = self._parts(path)
        node = self._root
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = node.get(parts[-1], "") + content

    def read_content_from_file(self, path):
        return self._walk(self._parts(path))
