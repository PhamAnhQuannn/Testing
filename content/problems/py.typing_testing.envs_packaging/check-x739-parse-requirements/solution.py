def parse_requirements(lines):
    ops = ["==", ">=", "<=", "~=", "!=", ">", "<"]
    out = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        for i, ch in enumerate(line):
            if ch == "#" and i > 0 and line[i - 1].isspace():
                line = line[:i].strip()
                break
        if not line:
            continue
        found = None
        for i in range(len(line)):
            for op in ops:
                if line.startswith(op, i):
                    found = (i, op)
                    break
            if found:
                break
        if found:
            i, op = found
            name = line[:i].strip()
            version = line[i + len(op) :].strip()
        else:
            name, op, version = line, "", ""
        name = name.split("[")[0].strip()
        out.append([name, op, version])
    return out
