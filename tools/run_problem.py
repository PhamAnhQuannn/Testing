"""Run a solution against a problem's tests with the shared harness.

    uv run python tools/run_problem.py content/problems/<subtopic>/<slug> \\
        [--solution wrong/no_count.py] [--tests sample|hidden|all] [--time-factor 3]

Two engines run the very same `harness.py`:

* `native` runs it in a child CPython process;
* `pyodide` runs it under Pyodide in Node (tools/pyodide-node/run.mjs), the closest thing to the
  browser worker that CI can run. It needs `npm ci` in tools/pyodide-node first. Its per-test
  limit is `limits.time_ms x limits.time_multiplier.pyodide` (SPEC 6.2).

Either way the parent process enforces the per-test time limit and kills a runaway child.
"""

import argparse
import json
import os
import select
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from common import ROOT, load_yaml, read_jsonl

HARNESS = ROOT / "apps/web/src/runner/pyodide/harness.py"
STARTUP_GRACE_S = 2.0  # interpreter start-up and request parsing, before the first test
PYODIDE_STARTUP_GRACE_S = 30.0  # Node + loading the WASM runtime, generous for cold CI runners
PYODIDE_DIR = ROOT / "tools/pyodide-node"
ENGINES = ("native", "pyodide")


def _failure(test_id, verdict, error, elapsed_ms=0.0):
    return {
        "id": test_id,
        "verdict": verdict,
        "got": None,
        "error": error,
        "stdout": "",
        "stderr": "",
        "elapsed_ms": elapsed_ms,
    }


def parse_result(line: bytes) -> dict | None:
    """A harness result line, or None for anything else that reached the channel."""
    try:
        result = json.loads(line)
    except ValueError:
        return None
    return result if isinstance(result, dict) and "verdict" in result else None


def overall_verdict(results: list[dict]) -> str:
    return next((r["verdict"] for r in results if r["verdict"] != "AC"), "AC")


def _run_child(
    command: list[str], code: str, io: dict, tests: list[dict], time_limit_ms: float, grace_s: float
) -> dict:
    """Run `tests` in a child process; a test over `time_limit_ms` ends the run with TLE."""
    request = json.dumps({"code": code, "io": io, "tests": tests}).encode()
    limit_s = time_limit_ms / 1000
    results: list[dict] = []
    buffer = b""
    started = time.monotonic()
    with tempfile.TemporaryFile() as stderr:
        proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=stderr,
            bufsize=0,
        )
        try:
            proc.stdin.write(request)
            proc.stdin.close()
            deadline = started + grace_s + limit_s
            while len(results) < len(tests) and not (results and results[-1]["verdict"] == "CE"):
                ready = select.select([proc.stdout], [], [], max(0.0, deadline - time.monotonic()))
                if not ready[0]:
                    results.append(
                        _failure(tests[len(results)]["id"], "TLE", "time limit exceeded")
                    )
                    break
                chunk = os.read(proc.stdout.fileno(), 1 << 16)
                if not chunk:
                    stderr.seek(0)
                    detail = stderr.read().decode(errors="replace")[-500:]
                    results.append(
                        _failure(tests[len(results)]["id"], "RE", f"runner exited: {detail}")
                    )
                    break
                *lines, buffer = (buffer + chunk).split(b"\n")
                for line in lines:
                    result = parse_result(line)
                    if result is not None:
                        results.append(result)
                        deadline = time.monotonic() + limit_s
        finally:
            proc.kill()
            proc.wait()
    return {
        "verdict": overall_verdict(results),
        "results": results,
        "elapsed_ms": round((time.monotonic() - started) * 1000, 3),
    }


def run_native(code: str, io: dict, tests: list[dict], time_limit_ms: float) -> dict:
    """Run `tests` with harness.py in a child CPython process."""
    command = [sys.executable, "-I", str(HARNESS)]
    return _run_child(command, code, io, tests, time_limit_ms, STARTUP_GRACE_S)


def pyodide_available() -> bool:
    return (PYODIDE_DIR / "node_modules/pyodide/pyodide.mjs").is_file()


def run_pyodide(code: str, io: dict, tests: list[dict], time_limit_ms: float) -> dict:
    """Run `tests` with harness.py under Pyodide in Node; same result shape as `run_native`."""
    if not pyodide_available():
        raise RuntimeError("Pyodide is not installed: run `npm ci` in tools/pyodide-node")
    command = ["node", str(PYODIDE_DIR / "run.mjs"), str(HARNESS)]
    return _run_child(command, code, io, tests, time_limit_ms, PYODIDE_STARTUP_GRACE_S)


def run_engine(engine: str, code: str, io: dict, tests: list[dict], time_limit_ms: float) -> dict:
    runner = {"native": run_native, "pyodide": run_pyodide}[engine]
    return runner(code, io, tests, time_limit_ms)


def engine_limit_ms(problem: dict, engine: str) -> float:
    """Per-test limit for `engine`: Pyodide is allowed `time_multiplier.pyodide` times longer."""
    limits = problem["limits"]
    factor = limits["time_multiplier"]["pyodide"] if engine == "pyodide" else 1
    return limits["time_ms"] * factor


def load_tests(problem_dir: Path, problem: dict, which: str) -> list[dict]:
    names = ["sample", "hidden"] if which == "all" else [which]
    return [t for name in names for t in read_jsonl(problem_dir / problem["tests"][name])]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("problem_dir", type=Path)
    parser.add_argument("--solution", default="solution.py", help="file relative to problem_dir")
    parser.add_argument("--tests", choices=["sample", "hidden", "all"], default="all")
    parser.add_argument("--tag", help="only run tests carrying this tag, e.g. stress")
    parser.add_argument("--engine", choices=ENGINES, default="native")
    parser.add_argument("--time-factor", type=float, default=1.0, help="multiplies limits.time_ms")
    args = parser.parse_args()

    problem = load_yaml(args.problem_dir / "problem.yaml")
    code = (args.problem_dir / args.solution).read_text(encoding="utf-8")
    tests = load_tests(args.problem_dir, problem, args.tests)
    if args.tag:
        tests = [t for t in tests if args.tag in t.get("tags", [])]
    limit_ms = engine_limit_ms(problem, args.engine) * args.time_factor
    run = run_engine(args.engine, code, problem["io"], tests, limit_ms)
    for r in run["results"]:
        print(f"{r['verdict']:<4} {r['id']}  {r['elapsed_ms']} ms  {r['error']}".rstrip())
    print(f"verdict: {run['verdict']}")
    return 0 if run["verdict"] == "AC" else 1


if __name__ == "__main__":
    sys.exit(main())
