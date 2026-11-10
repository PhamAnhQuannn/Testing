def final_cwd(start, cmds):
    parts = [p for p in start.split("/") if p]
    for cmd in cmds:
        tokens = cmd.split()
        if not tokens or tokens[0] != "cd":
            continue
        if len(tokens) == 1:
            parts = []
            continue
        arg = tokens[1]
        if arg.startswith("/"):
            parts = [p for p in arg.split("/") if p]
            continue
        for seg in arg.split("/"):
            if seg in ("", "."):
                continue
            if seg == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(seg)
    return "/" + "/".join(parts)
