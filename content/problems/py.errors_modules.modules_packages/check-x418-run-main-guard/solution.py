def run_both(code):
    result = []
    for name in ("__main__", "mymod"):
        log = []
        exec(code, {"__name__": name, "log": log})
        result.append(log)
    return result
