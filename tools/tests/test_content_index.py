import re

from common import CONTENT, ROOT, load_json, load_yaml
from gen_lesson_stubs import build_stub, objectives_from
from sync_tree import build_assumed, mvp_ids
from validate_content import schema_errors

SUBTOPICS = load_json(CONTENT / "index/subtopics.json")["subtopics"]


def spec_table_ids() -> list[str]:
    """The ids of the SPEC 4.1 table, in order."""
    text = (ROOT / "docs/SPEC.md").read_text(encoding="utf-8")
    section = text[text.index("### 4.1 ") : text.index("### 4.2 ")]
    return re.findall(r"^\| \d+ \| \d+ \| `([^`]+)` \|", section, flags=re.M)


def test_index_holds_the_40_subtopics_of_spec_4_1():
    ids = [s["id"] for s in SUBTOPICS]
    assert len(ids) == 40
    assert ids == spec_table_ids()


def test_every_subtopic_has_a_lesson_file_named_after_it():
    for s in SUBTOPICS:
        assert (CONTENT / "lessons" / s["section"] / f"{s['id']}.yaml").is_file()


def test_assumed_prerequisites():
    assert load_json(CONTENT / "index/assumed.json")["assumed"] == [
        "cs.onramp.computer_programming_model"
    ]


def test_mvp_ids_skip_behavioural_nodes_and_count_each_id_once():
    plan = {
        "days": [
            {"subtopics": [{"id": "py.a.b"}, {"id": "bh.x.y"}]},
            {"subtopics": [{"id": "py.a.b"}, {"id": "dsa.c.d"}]},
            {"subtopics": [{"id": "late.e.f"}]},
        ]
    }
    assert mvp_ids(plan) == ["py.a.b", "dsa.c.d", "late.e.f"]


def test_unplanned_outside_prerequisite_is_an_error():
    node = {"id": "py.a.b", "prerequisites": ["cs.x.y"], "lang_prereqs": {"python": []}}
    plan = {"selection": {"assumed_known": []}}
    try:
        build_assumed([node], plan)
    except SystemExit as error:
        assert "cs.x.y" in str(error)
    else:
        raise AssertionError("expected SystemExit")


def test_objectives_always_have_two_to_four_sentences():
    for s in SUBTOPICS:
        assert 2 <= len(objectives_from(s["mastery_bar_vi"])) <= 4, s["id"]


def test_stub_matches_the_lesson_schema():
    schema = load_json(CONTENT / "schemas/lesson.schema.json")
    stub = build_stub(SUBTOPICS[0], "0" * 64, "2026-01-01")
    assert schema_errors(stub, schema) == []
    assert schema_errors(load_yaml(CONTENT / "lessons/py/py.core.loops.yaml"), schema) == []
