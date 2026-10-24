"""Validate everything under content/ (SPEC 4.4). Exit code 1 when anything is wrong.

    uv run python tools/validate_content.py [--content content]

Implemented so far: JSON Schemas, ids and prerequisites, lesson code blocks, and every
per-problem check (generated hidden tests, reference solution, brute-force cross-check, wrong and
slow solutions, time limits, starter code). Still to come: `convert_checks.py` item checks
(mastery_check ids, level-2 write_code rule), the public-bundle `rewrite_required` gate and the
Pyodide engine (T1.0 / M1).
"""

import argparse
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import best_match

from common import CONTENT, load_json, load_yaml, read_jsonl
from gen_hidden import generate_hidden, load_generator
from run_problem import load_tests, run_native

SOLUTION_TIME_SHARE = 0.3  # solution.py must use at most this share of limits.time_ms
SLOW_TIME_FACTOR = 3  # slow/*.py must still be running after this many times limits.time_ms
MIN_SAMPLES = 3
MIN_HIDDEN = {"practice": 8, "check": 5, "mock": 8}
MAX_HIDDEN_BYTES = 1_000_000
CROSS_CHECK_CASES = 200
CROSS_CHECK_SEED = 20260101
SNIPPET_TIME_MS = 5000
GRADED_TYPES = {"quiz_mcq", "quiz_fill", "predict_output"}


def schema_errors(instance, schema: dict) -> list[str]:
    errors = []
    for error in Draft202012Validator(schema).iter_errors(instance):
        if error.validator in ("oneOf", "anyOf") and error.context:
            error = best_match(error.context) or error
        where = "/".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(f"{where}: {error.message}")
    return errors


class Validator:
    def __init__(self, content: Path):
        self.content = content
        self.errors: list[str] = []
        self.schemas = {
            name: load_json(content / "schema" / f"{name}.schema.json")
            for name in ("lesson", "problem", "check")
        }

    def fail(self, path: Path, message: str) -> None:
        self.errors.append(f"{path.relative_to(self.content)}: {message}")

    def check_schema(self, path: Path, instance, name: str, definition: str | None = None) -> bool:
        schema = self.schemas[name]
        if definition:
            schema = {"$defs": schema["$defs"], "$ref": f"#/$defs/{definition}"}
        errors = schema_errors(instance, schema)
        for message in errors:
            self.fail(path, message)
        return not errors

    # --- index -------------------------------------------------------------------------------

    def check_index(self) -> list[dict]:
        index = self.content / "index"
        subtopics = load_json(index / "subtopics.json")["subtopics"]
        assumed = set(load_json(index / "assumed.json")["assumed"])
        ids = [s["id"] for s in subtopics]
        if len(set(ids)) != len(ids):
            self.fail(index / "subtopics.json", "duplicate subtopic ids")
        prerequisites = {}
        for s in subtopics:
            needs = set(s["prerequisites"]) | set(s["lang_prereqs"]["python"] or [])
            unknown = needs - set(ids) - assumed
            if unknown:
                self.fail(
                    index / "subtopics.json", f"{s['id']}: unknown prerequisites {sorted(unknown)}"
                )
            prerequisites[s["id"]] = needs & set(ids)
        cycle = find_cycle(prerequisites)
        if cycle:
            self.fail(index / "subtopics.json", "prerequisite cycle: " + " -> ".join(cycle))
        return subtopics

    # --- lessons -----------------------------------------------------------------------------

    def check_lessons(self, subtopics: list[dict], problem_ids: set[str]) -> int:
        ids = {s["id"] for s in subtopics}
        files = sorted((self.content / "lessons").glob("*/*.yaml"))
        for path in files:
            lesson = load_yaml(path)
            if not self.check_schema(path, lesson, "lesson"):
                continue
            if lesson["id"] not in ids:
                self.fail(path, f"id {lesson['id']} is not in content/index/subtopics.json")
            if path.stem != lesson["id"] or path.parent.name != lesson["id"].split(".")[0]:
                self.fail(path, "file must be lessons/<section>/<id>.yaml")
            self.check_lesson_blocks(path, lesson, problem_ids)
        missing = ids - {p.stem for p in files}
        if missing:
            self.fail(self.content / "lessons", f"missing lessons: {sorted(missing)}")
        return len(files)

    def check_lesson_blocks(self, path: Path, lesson: dict, problem_ids: set[str]) -> None:
        blocks = lesson["blocks"]
        block_ids = [b["id"] for b in blocks]
        if len(set(block_ids)) != len(block_ids):
            self.fail(path, "duplicate block ids")
        referenced = lesson["problems"]["practice"] + lesson["problems"]["extra"]
        referenced += [b["problem_id"] for b in blocks if b["type"] == "problem_ref"]
        for problem_id in sorted(set(referenced) - problem_ids):
            self.fail(path, f"unknown problem {problem_id}")
        graded = [b for b in blocks if b["type"] in GRADED_TYPES and b.get("graded", True)]
        if lesson["status"] != "draft" and len(graded) < lesson["checkpoint"]["min_items"]:
            self.fail(path, f"needs at least {lesson['checkpoint']['min_items']} graded blocks")
        for block in blocks:
            for message in block_code_errors(block):
                self.fail(path, f"block {block['id']}: {message}")

    # --- problems ----------------------------------------------------------------------------

    def problem_dirs(self) -> list[Path]:
        return sorted(p.parent for p in (self.content / "problems").glob("*/*/problem.yaml"))

    def check_problems(self, subtopics: list[dict]) -> int:
        dirs = self.problem_dirs()
        for directory in dirs:
            self.check_problem(directory, {s["id"] for s in subtopics})
        return len(dirs)

    def check_problem(self, directory: Path, subtopic_ids: set[str]) -> None:
        yaml_path = directory / "problem.yaml"
        problem = load_yaml(yaml_path)
        if not self.check_schema(yaml_path, problem, "problem"):
            return
        if problem["id"] != directory.name:
            self.fail(directory, "directory name must equal the problem id")
        if problem["subtopic_id"] != directory.parent.name:
            self.fail(directory, "problem must live in problems/<subtopic_id>/")
        for sub in [problem["subtopic_id"], *problem["secondary_subtopics"]]:
            if sub not in subtopic_ids:
                self.fail(directory, f"unknown subtopic {sub}")
        paths = {
            "solution": directory / problem["solution"]["file"],
            "sample": directory / problem["tests"]["sample"],
            "hidden": directory / problem["tests"]["hidden"],
            "generator": directory / problem["tests"]["generator"],
        }
        missing = [name for name, path in paths.items() if not path.is_file()]
        for name in missing:
            self.fail(directory, f"missing {name} file {paths[name].relative_to(directory)}")
        if missing:
            return
        if not self.check_test_files(directory, problem, paths):
            return
        self.check_generated_hidden(directory, paths["hidden"])
        tests = load_tests(directory, problem, "all")
        self.check_reference(directory, problem, paths["solution"], tests)
        self.check_cross(directory, problem, paths["generator"], paths["solution"])
        self.check_variants(directory, problem, tests)
        self.check_starter(directory, problem, tests)

    def check_test_files(self, directory: Path, problem: dict, paths: dict[str, Path]) -> bool:
        ok = True
        ids = []
        for name in ("sample", "hidden"):
            rows = read_jsonl(paths[name])
            ids += [row.get("id") for row in rows]
            for row in rows:
                ok &= self.check_schema(paths[name], row, "problem", "test_case")
            floor = MIN_SAMPLES if name == "sample" else MIN_HIDDEN[problem["kind"]]
            if len(rows) < floor:
                self.fail(directory, f"{name} has {len(rows)} tests, needs at least {floor}")
            if name == "hidden" and not any("edge" in row.get("tags", []) for row in rows):
                self.fail(directory, "hidden tests need at least one test tagged 'edge'")
        if len(set(ids)) != len(ids):
            self.fail(directory, "test ids are not unique across sample and hidden")
        if paths["hidden"].stat().st_size > MAX_HIDDEN_BYTES:
            self.fail(directory, f"hidden tests exceed {MAX_HIDDEN_BYTES} bytes")
        return ok

    def check_generated_hidden(self, directory: Path, hidden: Path) -> None:
        try:
            generated = generate_hidden(directory)
        except RuntimeError as error:
            self.fail(directory, str(error))
            return
        if generated != read_jsonl(hidden):
            self.fail(directory, "hidden.jsonl is stale: re-run tools/gen_hidden.py")

    def check_reference(self, directory: Path, problem: dict, solution: Path, tests: list[dict]):
        limit_ms = problem["limits"]["time_ms"]
        run = run_native(solution.read_text(encoding="utf-8"), problem["io"], tests, limit_ms)
        for result in run["results"]:
            if result["verdict"] != "AC":
                self.fail(directory, f"solution {result['verdict']} on {result['id']}")
            elif result["elapsed_ms"] > SOLUTION_TIME_SHARE * limit_ms:
                self.fail(
                    directory,
                    f"solution takes {result['elapsed_ms']} ms on {result['id']}, "
                    f"over {SOLUTION_TIME_SHARE} x time_ms",
                )

    def check_cross(self, directory: Path, problem: dict, generator: Path, solution: Path) -> None:
        brute = directory / "brute.py"
        if not brute.is_file():
            if problem["difficulty"] != "easy":
                self.fail(directory, "brute.py is required for medium and hard problems")
            return
        inputs = load_generator(generator).small_inputs(CROSS_CHECK_SEED, CROSS_CHECK_CASES)
        cases = [{"id": f"c{i}", "args": args} for i, args in enumerate(inputs)]
        limit_ms = problem["limits"]["time_ms"]
        expected = run_native(brute.read_text(encoding="utf-8"), problem["io"], cases, limit_ms)
        if expected["verdict"] != "AC":
            self.fail(directory, f"brute.py {expected['verdict']} on its own small inputs")
            return
        checked = [
            c | {"expected": r["got"]} for c, r in zip(cases, expected["results"], strict=True)
        ]
        run = run_native(solution.read_text(encoding="utf-8"), problem["io"], checked, limit_ms)
        for result in run["results"]:
            if result["verdict"] != "AC":
                case = next(c for c in cases if c["id"] == result["id"])
                self.fail(directory, f"solution disagrees with brute.py on args {case['args']}")
                return

    def check_variants(self, directory: Path, problem: dict, tests: list[dict]) -> None:
        limit_ms = problem["limits"]["time_ms"]
        for wrong in sorted((directory / "wrong").glob("*.py")):
            run = run_native(wrong.read_text(encoding="utf-8"), problem["io"], tests, limit_ms)
            if run["verdict"] == "CE":
                self.fail(directory, f"{wrong.relative_to(directory)} does not compile")
            elif run["verdict"] == "AC":
                self.fail(directory, f"{wrong.relative_to(directory)} passes every test")
        stress = [t for t in tests if "stress" in t.get("tags", [])]
        for slow in sorted((directory / "slow").glob("*.py")):
            name = slow.relative_to(directory)
            if not stress:
                self.fail(directory, f"{name} needs hidden tests tagged 'stress'")
                continue
            run = run_native(
                slow.read_text(encoding="utf-8"), problem["io"], stress, limit_ms * SLOW_TIME_FACTOR
            )
            if run["verdict"] != "TLE":
                self.fail(
                    directory,
                    f"{name} must exceed {SLOW_TIME_FACTOR} x time_ms, got {run['verdict']}",
                )

    def check_starter(self, directory: Path, problem: dict, tests: list[dict]) -> None:
        run = run_native(
            problem["starter"]["python"], problem["io"], tests, problem["limits"]["time_ms"]
        )
        if run["verdict"] == "CE":
            self.fail(directory, "starter code does not compile")
        elif run["verdict"] == "AC":
            self.fail(directory, "starter code already passes every test")

    # --- whole tree --------------------------------------------------------------------------

    def run(self) -> dict[str, int]:
        subtopics = self.check_index()
        problem_ids = {p.name for p in self.problem_dirs()}
        counts = {
            "lessons": self.check_lessons(subtopics, problem_ids),
            "problems": self.check_problems(subtopics),
        }
        for path in sorted((self.content / "checks").glob("*.yaml")):
            self.check_schema(path, load_yaml(path), "check")
        return counts


def block_code_errors(block: dict) -> list[str]:
    """Run a lesson block's code: outputs must match; exercise solutions pass, starters fail."""
    kind = block["type"]
    if kind == "code_exercise":
        return exercise_errors(block)
    runnable_sample = kind == "code_sample" and block["runnable"] and "expected_output" in block
    if not (runnable_sample or kind == "predict_output"):
        return []
    test = {"id": block["id"], "expected": block["expected_output"]}
    run = run_native(block["code"], {"mode": "stdout"}, [test], SNIPPET_TIME_MS)
    if run["verdict"] == "AC":
        return []
    return [f"{run['verdict']}: expected {test['expected']!r}, got {run['results'][0]['got']!r}"]


def exercise_errors(block: dict) -> list[str]:
    """A code_exercise's solution must pass its tests and its starter must not."""
    io = {"mode": "function", "entry": block["entry"]}
    tests = [{"id": f"t{i}", **t} for i, t in enumerate(block["tests"], start=1)]
    errors = []
    solution = run_native(block["solution"], io, tests, SNIPPET_TIME_MS)
    if solution["verdict"] != "AC":
        errors.append(f"solution {solution['verdict']}")
    starter = run_native(block["starter"], io, tests, SNIPPET_TIME_MS)
    if starter["verdict"] == "CE":
        errors.append("starter does not compile")
    elif starter["verdict"] == "AC":
        errors.append("starter already passes every test")
    return errors


def find_cycle(graph: dict[str, set[str]]) -> list[str] | None:
    done: set[str] = set()

    def visit(node: str, path: list[str]) -> list[str] | None:
        if node in path:
            return [*path[path.index(node) :], node]
        if node in done:
            return None
        for parent in sorted(graph[node]):
            cycle = visit(parent, [*path, node])
            if cycle:
                return cycle
        done.add(node)
        return None

    return next((c for n in sorted(graph) if (c := visit(n, []))), None)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--content", type=Path, default=CONTENT)
    args = parser.parse_args()
    validator = Validator(args.content)
    counts = validator.run()
    for error in validator.errors:
        print(f"ERROR {error}")
    if validator.errors:
        print(f"{len(validator.errors)} problem(s) found")
        return 1
    print(f"content OK: {counts['lessons']} lessons, {counts['problems']} problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
