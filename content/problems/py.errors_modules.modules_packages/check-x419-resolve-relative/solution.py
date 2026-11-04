def resolve_relative(package, level, name):
    if level == 0:
        return name
    parts = package.split(".") if package else []
    if level > len(parts):
        return "error"
    base = ".".join(parts[: len(parts) - (level - 1)])
    if name:
        return base + "." + name
    return base
