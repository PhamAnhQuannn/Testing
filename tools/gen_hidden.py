"""Generate a problem's hidden tests: inputs come from tests/gen.py, `expected` from solution.py.

    uv run python tools/gen_hidden.py content/problems/<subtopic>/<slug>

gen.py exports `hidden_inputs()` (dicts with id, args, tags and, for class_ops mode, ops) and
`small_inputs(seed, n)`
(argument lists of at most 12 elements, used by the brute-force cross-check). It is deterministic,
so regenerating must reproduce the committed hidden.jsonl.
"""

import argparse
import importlib.util
from pathlib import Path

from common import dump_jsonl, load_yaml
from run_problem import run_native

GENERATION_TIME_FACTOR = 10  # the reference solution only has to finish, not to be fast


def load_generator(path: Path):
    spec = importlib.util.spec_from_file_location("problem_gen", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generate_hidden(problem_dir: Path) -> list[dict]:
    """Return the hidden tests, with `expected` recorded from the reference solution."""
    problem = load_yaml(problem_dir / "problem.yaml")
    inputs = load_generator(problem_dir / problem["tests"]["generator"]).hidden_inputs()
    code = (problem_dir / problem["solution"]["file"]).read_text(encoding="utf-8")
    limit_ms = problem["limits"]["time_ms"] * GENERATION_TIME_FACTOR
    run = run_native(code, problem["io"], inputs, limit_ms)
    failures = [r for r in run["results"] if r["verdict"] != "AC"]
    if failures or len(run["results"]) != len(inputs):
        raise RuntimeError(f"reference solution failed while generating: {failures}")
    return [
        {"id": t["id"], **extra_keys(t), "args": t["args"], "expected": r["got"], "tags": t["tags"]}
        for t, r in zip(inputs, run["results"], strict=True)
    ]


def extra_keys(test: dict) -> dict:
    """`ops` (class_ops mode) and `stdin` belong to the test, so they must reach hidden.jsonl."""
    return {key: test[key] for key in ("ops", "stdin") if key in test}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("problem_dir", type=Path)
    args = parser.parse_args()
    problem = load_yaml(args.problem_dir / "problem.yaml")
    tests = generate_hidden(args.problem_dir)
    path = args.problem_dir / problem["tests"]["hidden"]
    path.write_text(dump_jsonl(tests), encoding="utf-8")
    print(f"wrote {len(tests)} hidden tests to {path}")


if __name__ == "__main__":
    main()
