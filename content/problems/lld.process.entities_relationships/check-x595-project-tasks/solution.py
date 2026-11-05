class Task:
    """Entity owned by a Project (composition: no Project, no Task)."""

    def __init__(self, name):
        self.name = name
        self.done = False


class Project:
    """Aggregate root: has-a collection of Task entities and owns the behaviour."""

    def __init__(self, name):
        self.name = name
        self._tasks = {}

    def add_task(self, name):
        if name not in self._tasks:
            self._tasks[name] = Task(name)

    def complete(self, name):
        task = self._tasks.get(name)
        if task is not None:
            task.done = True

    def pending(self):
        return sum(1 for t in self._tasks.values() if not t.done)

    def done_names(self):
        return sorted(t.name for t in self._tasks.values() if t.done)
