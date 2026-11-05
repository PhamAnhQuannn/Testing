def cell_value(cells, target):
    memo = {}

    def value(name):
        if name in memo:
            return memo[name]
        content = cells[name]
        if isinstance(content, int):
            result = content
        else:
            result = 0
            for ref in content[1:].split("+"):
                result += value(ref)
        memo[name] = result
        return result

    return value(target)
