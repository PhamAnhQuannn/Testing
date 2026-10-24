"""Run a solution against a problem's tests with the shared harness.

    uv run python tools/run_problem.py content/problems/<subtopic>/<slug> \\
        [--solution wrong/no_count.py] [--tests sample|hidden|all] [--time-factor 3]

Only the native engine exists so far: it runs `harness.py` in a child Python process and
enforces the per-test time limit like the browser worker will. The Pyodide engine comes with T1.0.
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


def overall_verdict(results: list[dict]) -> str:
    return next((r["verdict"] for r in results if r["verdict"] != "AC"), "AC")


def run_native(code: str, io: dict, tests: list[dict], time_limit_ms: float) -> dict:
    """Run `tests` in a child process; a test over `time_limit_ms` ends the run with TLE."""
    request = json.dumps({"code": code, "io": io, "tests": tests}).encode()
    limit_s = time_limit_ms / 1000
    results: list[dict] = []
    buffer = b""
    started = time.monotonic()
    with tempfile.TemporaryFile() as stderr:
        proc = subprocess.Popen(
            [sys.executable, "-I", str(HARNESS)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=stderr,
            bufsize=0,
        )
        try:
            proc.stdin.write(request)
            proc.stdin.close()
            deadline = started + STARTUP_GRACE_S + limit_s
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
                    results.append(json.loads(line))
                    deadline = time.monotonic() + limit_s
        finally:
            proc.kill()
            proc.wait()
    return {
        "verdict": overall_verdict(results),
        "results": results,
        "elapsed_ms": round((time.monotonic() - started) * 1000, 3),
    }


def load_tests(problem_dir: Path, problem: dict, which: str) -> list[dict]:
    names = ["sample", "hidden"] if which == "all" else [which]
    return [t for name in names for t in read_jsonl(problem_dir / problem["tests"][name])]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("problem_dir", type=Path)
    parser.add_argument("--solution", default="solution.py", help="file relative to problem_dir")
    parser.add_argument("--tests", choices=["sample", "hidden", "all"], default="all")
    parser.add_argument("--engine", choices=["native"], default="native")
    parser.add_argument("--time-factor", type=float, default=1.0, help="multiplies limits.time_ms")
    args = parser.parse_args()

    problem = load_yaml(args.problem_dir / "problem.yaml")
    code = (args.problem_dir / args.solution).read_text(encoding="utf-8")
    tests = load_tests(args.problem_dir, problem, args.tests)
    limit_ms = problem["limits"]["time_ms"] * args.time_factor
    run = run_native(code, problem["io"], tests, limit_ms)
    for r in run["results"]:
        print(f"{r['verdict']:<4} {r['id']}  {r['elapsed_ms']} ms  {r['error']}".rstrip())
    print(f"verdict: {run['verdict']}")
    return 0 if run["verdict"] == "AC" else 1


if __name__ == "__main__":
    sys.exit(main())
