"""tools/convert_checks.py: assessment.json -> content/checks + `kind: check` problems."""

import shutil

import pytest

from check_specs import EXTRA_INPUTS, SPECIAL
from common import CONTENT, dump_yaml, load_json, load_yaml, read_jsonl
from convert_checks import ASSESSMENT, ConversionError, build_checks, convert, render_checks
from validate_content import Validator, schema_errors

ITEMS = load_json(ASSESSMENT)["items"]
MVP = {s["id"] for s in load_json(CONTENT / "index/subtopics.json")["subtopics"]}
OUTSIDE = next(i for i in ITEMS if i["type"] == "write_code" and i["subtopic_id"] not in MVP)
# simple function, dict item, class item, linked-list item, plus a read_code and a concept item
SAMPLE_IDS = {"Q006", "Q023", "Q077", "Q079", "Q007", "Q001", OUTSIDE["id"]}


def make_content(tmp_path):
    root = tmp_path / "content"
    (root / "index").mkdir(parents=True)
    shutil.copy(CONTENT / "index/subtopics.json", root / "index/subtopics.json")
    shutil.copytree(CONTENT / "schemas", root / "schemas")
    return root


def snapshot(root):
    return {
        str(p.relative_to(root)): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts
    }


@pytest.fixture(scope="module")
def converted(tmp_path_factory):
    root = make_content(tmp_path_factory.mktemp("convert"))
    counts = convert(ASSESSMENT, root, SAMPLE_IDS)
    first = snapshot(root)
    convert(ASSESSMENT, root, SAMPLE_IDS)
    return root, counts, first, snapshot(root)


def test_second_run_changes_nothing(converted):
    _, _, first, second = converted
    assert first == second


def test_counts_and_outside_mvp_item_is_skipped(converted):
    root, counts, _, _ = converted
    assert counts["items"] == 7
    assert counts["converted"] == 6
    assert counts["skipped"] == 1
    assert counts["check_problems"] == 4
    assert not list((root / "problems").glob(f"*/*{OUTSIDE['id'].lower()}"))
    assert not (root / "checks" / f"{OUTSIDE['subtopic_id']}.yaml").exists()


def test_checks_file_matches_the_schema_and_the_item(converted):
    root, _, _, _ = converted
    schema = load_json(root / "schemas/check.schema.json")
    data = load_yaml(root / "checks/py.datastructs.dict.yaml")
    assert schema_errors(data, schema) == []
    item = next(i for i in data["items"] if i["id"] == "Q023")
    source = next(i for i in ITEMS if i["id"] == "Q023")
    assert item == {
        "id": "Q023",
        "difficulty": 2,
        "type": "write_code",
        "minutes": 6,
        "prompt_md": source["prompt"],
        "problem_id": "check-q023",
        "rubric_md": source["rubric"],
    }


def test_read_code_and_concept_items_keep_their_fields(converted):
    root, _, _, _ = converted
    read = load_yaml(root / "checks/py.core.conditionals.yaml")["items"][0]
    assert (read["id"], read["type"]) == ("Q007", "read_code")
    source = next(i for i in ITEMS if i["id"] == "Q007")
    assert read["code"] == source["code"] and read["expected_output"] == source["expected_output"]
    concept = load_yaml(root / "checks/py.core.getting_started.yaml")["items"][0]
    assert concept["type"] == "concept" and concept["answer_md"]


def test_check_problem_is_a_time_boxed_check_with_recorded_expectations(converted):
    root, _, _, _ = converted
    directory = root / "problems/py.datastructs.dict/check-q023"
    problem = load_yaml(directory / "problem.yaml")
    assert (problem["id"], problem["kind"], problem["time_target_min"]) == (
        "check-q023",
        "check",
        6,
    )
    assert problem["io"]["entry"] == "two_sum"
    assert [p["name"] for p in problem["io"]["params"]] == ["nums", "target"]
    sample = read_jsonl(directory / "tests/sample.jsonl")
    hidden = read_jsonl(directory / "tests/hidden.jsonl")
    assert sample == [{"id": "s1", "args": [[2, 7, 11, 15], 9], "expected": [0, 1]}]
    assert len(hidden) >= 5
    assert any("edge" in t["tags"] for t in hidden)
    driver_call = next(t for t in hidden if t["args"] == [[3, 3], 6])
    assert driver_call["expected"] == [0, 1]  # the driver's other calls became hidden tests


def test_class_and_linked_list_items_use_the_matching_modes(converted):
    root, _, _, _ = converted
    stack = root / "problems/py.oop.classes_basics/check-q077"
    assert load_yaml(stack / "problem.yaml")["io"]["mode"] == "class_ops"
    assert all("ops" in t for t in read_jsonl(stack / "tests/hidden.jsonl"))
    node = root / "problems/dsa.linked_list.ll_basics/check-q079"
    io = load_yaml(node / "problem.yaml")["io"]
    assert io["params"] == [{"name": "head", "type": "list_node"}] and io["returns"] == "list_node"
    assert read_jsonl(node / "tests/sample.jsonl")[0]["expected"] == [4, 3, 2, 1]


def test_generated_problems_pass_the_validator(converted):
    root, _, _, _ = converted
    validator = Validator(root)
    for directory in validator.problem_dirs():
        validator.check_problem(directory, MVP)
    validator.check_check_files(MVP)
    assert validator.errors == []


def test_author_added_items_are_merged_after_the_converted_ones(tmp_path):
    root = make_content(tmp_path)
    extra = {
        "id": "X001",
        "difficulty": 2,
        "type": "concept",
        "minutes": 3,
        "prompt_md": "Giải thích.",
        "answer_md": "Đáp án.",
    }
    (root / "checks_extra").mkdir()
    path = root / "checks_extra/py.core.operators.yaml"
    path.write_text(dump_yaml({"subtopic_id": "py.core.operators", "items": [extra]}))
    convert(ASSESSMENT, root, {"Q006"})
    merged = load_yaml(root / "checks/py.core.operators.yaml")["items"]
    assert [i["id"] for i in merged] == ["Q006", "X001"]
    validator = Validator(root)
    validator.check_check_files(MVP)
    validator.check_extra_files(MVP)
    assert validator.errors == []
    path.write_text(
        dump_yaml({"subtopic_id": "py.core.operators", "items": [{**extra, "id": "Q006"}]})
    )
    with pytest.raises(ConversionError, match="clashes"):
        convert(ASSESSMENT, root, {"Q006"})


def test_committed_checks_are_up_to_date():
    """content/checks/* is exactly what the tool renders (no hand edits, no stale files)."""
    items = [i for i in ITEMS if i["subtopic_id"] in MVP]
    checks = build_checks(items, CONTENT)
    on_disk = {p.stem for p in (CONTENT / "checks").glob("*.yaml")}
    assert on_disk == set(checks)
    for subtopic_id, entries in checks.items():
        path = CONTENT / "checks" / f"{subtopic_id}.yaml"
        assert path.read_text(encoding="utf-8") == render_checks(subtopic_id, entries), path.name


def test_every_mvp_write_code_item_has_inputs():
    mvp_code = [i["id"] for i in ITEMS if i["type"] == "write_code" and i["subtopic_id"] in MVP]
    assert len(mvp_code) == 61
    assert [i for i in mvp_code if i not in EXTRA_INPUTS and i not in SPECIAL] == []
    assert sum(1 for i in ITEMS if i["subtopic_id"] in MVP and i["type"] != "write_code") == 51
