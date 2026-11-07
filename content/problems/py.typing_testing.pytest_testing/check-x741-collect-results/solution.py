def collect_results(tests):
    failures = []
    passed = 0
    for name, got, want in tests:
        if got == want:
            passed += 1
        else:
            failures.append(name)
    return {"passed": passed, "failed": len(failures), "failures": failures}
