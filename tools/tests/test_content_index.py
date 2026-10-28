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


EXTRA_MODULES = {"ml.llm", "ml.rag_agents", "ml.llm_eval_serving", "ml.system_design"}


def test_index_starts_with_the_40_subtopics_of_spec_4_1():
    ids = [s["id"] for s in SUBTOPICS]
    assert len(ids) == 165  # 40 plan (py/dsa/cs) + 86 sd + 39 ml (the AI-engineer LLM track)
    assert ids[:40] == spec_table_ids()


def test_extra_track_section_counts():
    sections = [s["section"] for s in SUBTOPICS]
    assert sections.count("sd") == 86
    assert sections.count("ml") == 39
    assert sum(1 for s in SUBTOPICS if s["module"] in EXTRA_MODULES) == 39


def test_every_plan_subtopic_has_a_lesson_file_named_after_it():
    # The py/dsa/cs MVP subtopics ship lessons. The System Design (sd) and AI-engineer (ml) tracks
    # are authored incrementally, so their lesson files may not exist yet.
    for s in SUBTOPICS:
        if s["section"] in ("py", "dsa", "cs"):
            assert (CONTENT / "lessons" / s["section"] / f"{s['id']}.yaml").is_file()


def test_assumed_prerequisites():
    assumed = load_json(CONTENT / "index/assumed.json")["assumed"]
    shipped = {s["id"] for s in SUBTOPICS}
    assert len(assumed) == 43  # prereqs of the sd + ml tracks that are not themselves shipped
    assert "cs.onramp.computer_programming_model" in assumed
    assert set(assumed).isdisjoint(shipped)
    assert assumed == sorted(assumed)


def test_mvp_ids_skip_behavioural_nodes_and_count_each_id_once():
    plan = {
        "days": [
            {"subtopics": [{"id": "py.a.b"}, {"id": "bh.x.y"}]},
            {"subtopics": [{"id": "py.a.b"}, {"id": "dsa.c.d"}]},
            {"subtopics": [{"id": "late.e.f"}]},
        ]
    }
    assert mvp_ids(plan) == ["py.a.b", "dsa.c.d", "late.e.f"]


def test_prerequisite_missing_from_the_tree_is_an_error():
    sub = {"id": "sd.a.b", "prerequisites": ["ghost.x.y"], "lang_prereqs": {"python": []}}
    nodes = {"sd.a.b": ("sd", "sd.a", {})}  # the prereq is not a node in the tree
    try:
        build_assumed([sub], nodes)
    except SystemExit as error:
        assert "ghost.x.y" in str(error)
    else:
        raise AssertionError("expected SystemExit")


def test_objectives_always_have_two_to_four_sentences():
    # Only for the sections whose lessons are authored from stubs (py/dsa/cs). The sd/ml tracks are
    # authored directly, so their mastery_bar_vi is not required to split into sentences here.
    for s in SUBTOPICS:
        if s["section"] in ("py", "dsa", "cs"):
            assert 2 <= len(objectives_from(s["mastery_bar_vi"])) <= 4, s["id"]


def test_stub_matches_the_lesson_schema():
    schema = load_json(CONTENT / "schemas/lesson.schema.json")
    stub = build_stub(SUBTOPICS[0], "0" * 64, "2026-01-01")
    assert schema_errors(stub, schema) == []
    assert schema_errors(load_yaml(CONTENT / "lessons/py/py.core.loops.yaml"), schema) == []
