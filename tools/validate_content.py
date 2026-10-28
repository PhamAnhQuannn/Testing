"""Validate everything under content/ (SPEC 4.4). Exit code 1 when anything is wrong.

    uv run python tools/validate_content.py [--content content]

Checks: JSON Schemas, ids and prerequisites, lesson code blocks (outputs, exercises, runnable
samples), lesson/problem/mastery-check references, at least 3 graded blocks per non-draft lesson,
a level-2 write_code check item for every non-draft lesson (content/checks, which tools/
convert_checks.py builds from the assessment plus content/checks_extra), and every
per-problem check (generated hidden tests, reference solution, brute-force cross-check,
wrong and slow solutions, time limits, starter code).

Options:
    --pyodide   also run each reference solution on its `stress` tests under Pyodide in Node
                (needs `npm ci` in tools/pyodide-node), so native and browser timing stay within
                `limits.time_multiplier.pyodide` of each other (SPEC 4.4 / 6.2).
    --public    the public-bundle gate: published problems must not still be `rewrite_required`.
"""

import argparse
import ast
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import best_match

from common import CONTENT, load_json, load_yaml, read_jsonl
from gen_hidden import generate_hidden, load_generator
from run_problem import engine_limit_ms, load_tests, run_native, run_pyodide
from sync_tree import EXTRA_MODULES, EXTRA_SECTIONS

SOLUTION_TIME_SHARE = 0.3  # solution.py must use at most this share of limits.time_ms
SLOW_TIME_FACTOR = 3  # slow/*.py must still be running after this many times limits.time_ms
MIN_SAMPLES = {"practice": 3, "check": 1, "mock": 3}  # SPEC 3.4: a check has 1 sample
MIN_HIDDEN = {"practice": 8, "check": 5, "mock": 8}
MAX_HIDDEN_BYTES = 1_000_000
CROSS_CHECK_CASES = 200
CROSS_CHECK_SEED = 20260101
SNIPPET_TIME_MS = 5000
GRADED_TYPES = {"quiz_mcq", "quiz_fill", "predict_output"}
MIN_GRADED_BLOCKS = 3
LEVELS = {"l1": 1, "l2": 2, "l3": 3}
# SPEC 3.4: once these subtopics have a lesson they need a level-2 write_code mastery item.
NEEDS_L2_WRITE_CODE = {
    "py.core.getting_started",
    "py.core.variables_types",
    "py.datastructs.tuple_namedtuple",
    "py.datastructs.copying_mutability",
    "py.functions.lambda_hof",
    "cs.complexity.big_o",
    "dsa.foundations.memory_model",
    "py.functions.scope_closures",
    "dsa.foundations.interview_method",
}


def schema_errors(instance, schema: dict) -> list[str]:
    errors = []
    for error in Draft202012Validator(schema).iter_errors(instance):
        if error.validator in ("oneOf", "anyOf") and error.context:
            error = best_match(error.context) or error
        where = "/".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(f"{where}: {error.message}")
    return errors


class Validator:
    def __init__(self, content: Path, *, pyodide: bool = False, public: bool = False):
        self.content = content
        self.pyodide = pyodide
        self.public = public
        self.errors: list[str] = []
        self._problems: dict[str, dict] | None = None
        self.checks: dict[str, dict[str, dict]] = {}  # subtopic id -> item id -> item
        self.schemas = {
            name: load_json(content / "schemas" / f"{name}.schema.json")
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

    def problem_meta(self) -> dict[str, dict]:
        """problem id -> problem.yaml, for every problem that loads."""
        if self._problems is None:
            self._problems = {}
            for directory in self.problem_dirs():
                problem = load_yaml(directory / "problem.yaml")
                if isinstance(problem, dict) and "id" in problem:
                    self._problems[problem["id"]] = problem
        return self._problems

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
            self.check_lesson_problems(path, lesson)
            self.check_mastery_refs(path, lesson)
        # Every subtopic must have a lesson EXCEPT the concept tracks (System Design + the
        # AI-engineer LLM track, sync_tree.EXTRA_*), which are authored incrementally; any lesson
        # that IS present is still validated by the loop above.
        required = {
            s["id"]
            for s in subtopics
            if s.get("section") not in EXTRA_SECTIONS and s.get("module") not in EXTRA_MODULES
        }
        missing = required - {p.stem for p in files}
        if missing:
            self.fail(self.content / "lessons", f"missing lessons: {sorted(missing)}")
        return len(files)

    def check_lesson_blocks(self, path: Path, lesson: dict, problem_ids: set[str]) -> None:
        blocks = lesson["blocks"]
        block_ids = [b["id"] for b in blocks]
        if len(set(block_ids)) != len(block_ids):
            self.fail(path, "duplicate block ids")
        listed = lesson["problems"]["practice"] + lesson["problems"]["extra"]
        refs = [b["problem_id"] for b in blocks if b["type"] == "problem_ref"]
        for problem_id in sorted(set(listed + refs) - problem_ids):
            self.fail(path, f"unknown problem {problem_id}")
        for problem_id in sorted(set(refs) & problem_ids - set(listed)):
            self.fail(path, f"problem_ref {problem_id} is not in problems.practice or extra")
        graded = [b for b in blocks if b["type"] in GRADED_TYPES and b.get("graded", True)]
        needed = max(MIN_GRADED_BLOCKS, lesson["checkpoint"]["min_items"])
        if lesson["status"] != "draft" and len(graded) < needed:
            self.fail(path, f"needs at least {needed} graded blocks, has {len(graded)}")
        for block in blocks:
            for message in block_code_errors(block):
                self.fail(path, f"block {block['id']}: {message}")

    def check_lesson_problems(self, path: Path, lesson: dict) -> None:
        """Problems a lesson lists belong to it; a published lesson only links published ones."""
        problems = self.problem_meta()
        refs = [b["problem_id"] for b in lesson["blocks"] if b["type"] == "problem_ref"]
        listed = lesson["problems"]["practice"] + lesson["problems"]["extra"]
        for problem_id in sorted({*listed, *refs}):
            problem = problems.get(problem_id)
            if problem is None:
                continue  # reported as unknown
            if lesson["id"] not in [problem.get("subtopic_id"), *problem["secondary_subtopics"]]:
                self.fail(path, f"problem {problem_id} belongs to {problem.get('subtopic_id')}")
            if lesson["status"] == "published" and problem.get("status") != "published":
                self.fail(path, f"published lesson links {problem['status']} problem {problem_id}")
        if lesson["status"] == "draft":
            return
        for problem_id, problem in sorted(problems.items()):
            if (
                problem.get("subtopic_id") == lesson["id"]
                and problem.get("kind") == "practice"
                and problem_id not in listed
            ):
                self.fail(path, f"practice problem {problem_id} is not in problems.practice/extra")

    def check_mastery_refs(self, path: Path, lesson: dict) -> None:
        """Every mastery_check id resolves to a checks/<subtopic>.yaml item of the same level."""
        items = self.checks.get(lesson["id"], {})
        for level, difficulty in LEVELS.items():
            for item_id in lesson["mastery_check"][level]:
                item = items.get(item_id)
                if item is None:
                    self.fail(path, f"mastery_check {level}: unknown item {item_id}")
                elif item["difficulty"] != difficulty:
                    self.fail(
                        path,
                        f"mastery_check {level}: {item_id} has difficulty {item['difficulty']}",
                    )
        if lesson["status"] == "draft":
            return
        section = lesson["id"].split(".")[0]
        module = ".".join(lesson["id"].split(".")[:2])
        concept_track = section in EXTRA_SECTIONS or module in EXTRA_MODULES
        has_wc2 = any(i["difficulty"] == 2 and i["type"] == "write_code" for i in items.values())
        if concept_track and not has_wc2:
            # A concept subtopic (System Design + the AI-engineer LLM track, no code) is gated by a
            # level-2 concept/read_code item instead of write_code (SPEC 5.2).
            if not any(i["difficulty"] == 2 for i in items.values()):
                self.fail(path, "concept subtopic needs a level-2 check item (SPEC 5.2)")
            if not lesson["mastery_check"]["l2"]:
                self.fail(path, "concept subtopic needs a level-2 mastery_check.l2 item (SPEC 5.2)")
            return
        if not has_wc2:
            self.fail(path, "needs a level-2 write_code item in content/checks (SPEC 3.4/4.4)")
        if lesson["id"] in NEEDS_L2_WRITE_CODE and not any(
            items.get(i, {}).get("type") == "write_code" for i in lesson["mastery_check"]["l2"]
        ):
            self.fail(path, "needs a level-2 write_code item in mastery_check.l2 (SPEC 3.4)")

    # --- mastery check files -----------------------------------------------------------------

    def check_check_files(self, subtopic_ids: set[str]) -> None:
        problems = self.problem_meta()
        seen: dict[str, Path] = {}
        for path in sorted((self.content / "checks").glob("*.yaml")):
            data = load_yaml(path)
            if not self.check_schema(path, data, "check"):
                continue
            if data["subtopic_id"] != path.stem or path.stem not in subtopic_ids:
                self.fail(path, "file must be checks/<subtopic_id>.yaml for a known subtopic")
            items = self.checks.setdefault(data["subtopic_id"], {})
            for item in data["items"]:
                if item["id"] in seen:
                    self.fail(path, f"item id {item['id']} also appears in {seen[item['id']].name}")
                seen[item["id"]] = path
                items[item["id"]] = item
                if item["type"] != "write_code":
                    continue
                problem = problems.get(item["problem_id"])
                if problem is None:
                    self.fail(path, f"{item['id']}: unknown problem {item['problem_id']}")
                elif problem.get("kind") != "check":
                    self.fail(
                        path, f"{item['id']}: problem {item['problem_id']} must be kind check"
                    )

    def check_extra_files(self, subtopic_ids: set[str]) -> None:
        """content/checks_extra/<id>.yaml holds author-added items; convert_checks.py merges them
        into content/checks/<id>.yaml, so each must appear there unchanged."""
        for path in sorted((self.content / "checks_extra").glob("*.yaml")):
            data = load_yaml(path)
            if not self.check_schema(path, data, "check"):
                continue
            if data["subtopic_id"] != path.stem or path.stem not in subtopic_ids:
                self.fail(path, "file must be checks_extra/<subtopic_id>.yaml for a known subtopic")
                continue
            merged = self.checks.get(data["subtopic_id"], {})
            for item in data["items"]:
                if merged.get(item["id"]) != item:
                    self.fail(path, f"item {item['id']} is not merged: run tools/convert_checks.py")

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
        if problem["io"].get("compare") == "custom":
            self.fail(
                directory, "io.compare custom is not supported yet: harness.py has no checker"
            )
            return
        if (
            self.public
            and problem["status"] == "published"
            and problem["source"].get("rewrite_required")
        ):
            self.fail(
                directory, "published problem still has source.rewrite_required (public bundle)"
            )
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
        self.check_first_example(directory, problem, load_tests(directory, problem, "sample"))
        tests = load_tests(directory, problem, "all")
        if not self.check_reference(directory, problem, paths["solution"], tests):
            return  # every remaining check compares against a working reference solution
        self.check_cross(directory, problem, paths["generator"], paths["solution"])
        hidden = load_tests(directory, problem, "hidden")
        if self.pyodide:
            self.check_pyodide(directory, problem, paths["solution"], hidden)
        self.check_variants(directory, problem, hidden)
        self.check_starter(directory, problem, tests)

    def check_test_files(self, directory: Path, problem: dict, paths: dict[str, Path]) -> bool:
        ok = True
        ids = []
        for name in ("sample", "hidden"):
            rows = read_jsonl(paths[name])
            ids += [row.get("id") for row in rows]
            for row in rows:
                ok &= self.check_schema(paths[name], row, "problem", "test_case")
            floor = (MIN_SAMPLES if name == "sample" else MIN_HIDDEN)[problem["kind"]]
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

    def check_first_example(self, directory: Path, problem: dict, samples: list[dict]) -> None:
        """The first statement example must be sample test 1 (function mode only)."""
        if problem["io"]["mode"] != "function":
            return
        example = problem["examples"][0]
        names = [p["name"] for p in problem["io"]["params"]]
        try:
            call = ast.parse(f"dict({example['input']})", mode="eval").body
            args = {kw.arg: ast.literal_eval(kw.value) for kw in call.keywords}
            output = json.loads(example["output"])
        except (SyntaxError, ValueError):
            self.fail(directory, "examples[0] input/output cannot be parsed")
            return
        if [args.get(n) for n in names] != samples[0]["args"] or output != samples[0]["expected"]:
            self.fail(directory, "examples[0] must be sample test 1")

    def check_reference(
        self, directory: Path, problem: dict, solution: Path, tests: list[dict]
    ) -> bool:
        limit_ms = problem["limits"]["time_ms"]
        run = run_native(solution.read_text(encoding="utf-8"), problem["io"], tests, limit_ms)
        failed = False
        for result in run["results"]:
            if result["verdict"] != "AC":
                detail = result["error"] if result["verdict"] == "CE" else f"on {result['id']}"
                self.fail(directory, f"solution {result['verdict']} {detail}")
                failed = True
            elif result["elapsed_ms"] > SOLUTION_TIME_SHARE * limit_ms:
                self.fail(
                    directory,
                    f"solution takes {result['elapsed_ms']} ms on {result['id']}, "
                    f"over {SOLUTION_TIME_SHARE} x time_ms",
                )
        return not failed

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

    def check_variants(self, directory: Path, problem: dict, hidden: list[dict]) -> None:
        limit_ms = problem["limits"]["time_ms"]
        for wrong in sorted((directory / "wrong").glob("*.py")):
            run = run_native(wrong.read_text(encoding="utf-8"), problem["io"], hidden, limit_ms)
            if run["verdict"] == "CE":
                self.fail(directory, f"{wrong.relative_to(directory)} does not compile")
            elif run["verdict"] == "AC":
                self.fail(directory, f"{wrong.relative_to(directory)} passes every hidden test")
        stress = [t for t in hidden if "stress" in t.get("tags", [])]
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

    def check_pyodide(
        self, directory: Path, problem: dict, solution: Path, hidden: list[dict]
    ) -> None:
        """The reference solution must also pass the stress tests in Pyodide, within its limit."""
        stress = [t for t in hidden if "stress" in t.get("tags", [])]
        if not stress:
            return
        limit_ms = engine_limit_ms(problem, "pyodide")
        run = run_pyodide(solution.read_text(encoding="utf-8"), problem["io"], stress, limit_ms)
        for result in run["results"]:
            if result["verdict"] != "AC":
                self.fail(
                    directory,
                    f"solution {result['verdict']} under Pyodide on {result['id']} "
                    f"(limit {limit_ms:g} ms): {result['error']}".rstrip(": "),
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
        self.check_check_files({s["id"] for s in subtopics})
        self.check_extra_files({s["id"] for s in subtopics})
        return {
            "lessons": self.check_lessons(subtopics, problem_ids),
            "problems": self.check_problems(subtopics),
        }


def block_code_errors(block: dict) -> list[str]:
    """Run a lesson block's code: outputs must match; exercise solutions pass, starters fail."""
    kind = block["type"]
    if kind == "code_exercise":
        return exercise_errors(block)
    runnable_sample = kind == "code_sample" and block["runnable"] and block["lang"] == "python"
    if not (runnable_sample or kind == "predict_output"):
        return []
    test = {"id": block["id"]}
    if "expected_output" in block:  # a runnable sample without one only has to run
        test["expected"] = block["expected_output"]
    run = run_native(block["code"], {"mode": "stdout"}, [test], SNIPPET_TIME_MS)
    if run["verdict"] == "AC":
        return []
    result = run["results"][0]
    if result["verdict"] in ("RE", "CE", "TLE"):
        return [f"{run['verdict']}: {result['error']}"]
    return [f"{run['verdict']}: expected {test['expected']!r}, got {result['got']!r}"]


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
    parser.add_argument("--pyodide", action="store_true", help="also run stress tests in Pyodide")
    parser.add_argument("--public", action="store_true", help="public bundle: no rewrite_required")
    args = parser.parse_args()
    validator = Validator(args.content, pyodide=args.pyodide, public=args.public)
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
