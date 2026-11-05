CYCLE = "#CYCLE"


def evaluate_sheet(cells):
    state = {}  # name -> 1 (visiting) / 2 (done)
    result = {}

    def visit(name):
        if state.get(name) == 2:
            return result[name]
        if state.get(name) == 1:
            return CYCLE
        state[name] = 1
        content = cells[name]
        if isinstance(content, int):
            value = content
        else:
            value = 0
            for ref in content[1:].split("+"):
                sub = visit(ref)
                if sub == CYCLE:
                    value = CYCLE
                elif value != CYCLE:
                    value += sub
        state[name] = 2
        result[name] = value
        return value

    for name in sorted(cells):
        visit(name)
    return {name: result[name] for name in sorted(cells)}
