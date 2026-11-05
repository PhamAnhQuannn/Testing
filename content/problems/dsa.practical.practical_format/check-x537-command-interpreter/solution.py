def run_kv(commands):
    store = {}
    out = []
    for line in commands:
        parts = line.split()
        op = parts[0]
        if op == "SET":
            store[parts[1]] = parts[2]
        elif op == "GET":
            out.append(store.get(parts[1], ""))
        elif op == "DEL":
            store.pop(parts[1], None)
    return out
