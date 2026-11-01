"""Shared PASS/FAIL driver for ``write_test`` items (web runner + content validator).

A ``write_test`` item asks the learner to write a test that catches a planted bug. The
runner assembles one module as ``implementation + "\n" + learner_test + "\n" + <this
file>`` and runs it in the harness ``function`` mode with entry ``_prep_run_tests``.

``_prep_run_tests`` runs every top-level ``test_*`` callable and returns ``"FAIL"`` if
any of them raised, else ``"PASS"``. Grading compares the *return value* (``exact``), so
anything the learner's test prints goes to stdout and is ignored. An item is AC only when
this returns ``"FAIL"`` against the buggy implementation (the test caught the bug) and
``"PASS"`` against the correct implementation (the test is not a false alarm).

This module is the single source of truth: the web runner imports it with ``?raw`` and
the validator reads it from disk, so both sides run byte-identical driver code. Keep it
dependency-free and side-effect-free on import.
"""


def _prep_run_tests():
    failed = False
    for _name, _fn in list(globals().items()):
        if _name.startswith("test_") and callable(_fn):
            try:
                _fn()
            except Exception:  # noqa: BLE001 - any raise means the test flagged a defect
                failed = True
    return "FAIL" if failed else "PASS"
