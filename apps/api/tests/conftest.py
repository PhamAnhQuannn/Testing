"""Test fixtures: a small synthetic content tree and an app on a temp data dir."""

from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.runtime import Runtime

T0 = datetime(2026, 11, 2, 3, 0, tzinfo=UTC)  # 10:00 in Asia/Ho_Chi_Minh


class Clock:
    def __init__(self, start: datetime = T0) -> None:
        self.now = start

    def __call__(self) -> datetime:
        return self.now

    def advance(self, **kw: float) -> None:
        self.now += timedelta(**kw)


def _sub(sid: str, order: int, prereqs: list[str], intern: int = 2) -> dict:
    return {
        "id": sid,
        "section": sid.split(".")[0],
        "module": ".".join(sid.split(".")[:2]),
        "name_vi": f"Mục {sid}",
        "order": order,
        "summary_vi": "tóm tắt",
        "mastery_bar_vi": "mức 3",
        "prerequisites": prereqs,
        "target_swe": {"intern": intern, "fresher": 3},
        "target_ai": {"intern": intern, "fresher": 3},
        "est_hours": 1.0,
        "plan_order": order,
    }


def _quiz(i: int, ans: str = "b") -> dict:
    return {
        "id": f"q{i}",
        "type": "quiz_mcq",
        "prompt_md": "?",
        "options": [{"id": "a", "text_md": "A"}, {"id": "b", "text_md": "B"}],
        "answer": [ans],
        "explain_md": f"vì {i}",
    }


def build_content(root: Path, *, status: str = "published") -> Path:
    (root / "index").mkdir(parents=True)
    subs = [
        _sub("py.a.one", 1, ["cs.assumed"]),
        _sub("py.a.two", 2, ["py.a.one"]),
        _sub("py.a.three", 3, ["py.a.two", "cs.outside"]),
    ]
    (root / "index" / "subtopics.json").write_text(json.dumps({"subtopics": subs}))
    (root / "index" / "assumed.json").write_text(json.dumps({"assumed": ["cs.assumed"]}))
    days = [
        {"day": 1, "subtopics": [{"id": "py.a.one"}, {"id": "py.a.two"}]},
        {"day": 2, "subtopics": [{"id": "py.a.three"}]},
    ]
    (root / "index" / "plan.json").write_text(json.dumps({"days": days}))

    lessons = root / "lessons" / "py"
    lessons.mkdir(parents=True)
    blocks = [
        {"id": "b01", "type": "text", "md": "hello"},
        _quiz(1),
        _quiz(2),
        {
            "id": "q3",
            "type": "quiz_fill",
            "prompt_md": "d.___(k)",
            "blanks": [{"accept": ["get"]}],
            "explain_md": "get",
        },
        {
            "id": "q4",
            "type": "predict_output",
            "code": "print(1)",
            "expected_output": "1",
            "explain_md": "một",
        },
        {
            "id": "ex1",
            "type": "code_exercise",
            "md": "x",
            "entry": "f",
            "starter": "def f(): pass",
            "tests": [{"args": [], "expected": 1}] * 3,
            "hint_md": "h",
            "solution": "def f(): return 1",
        },
    ]
    lesson = {
        "id": "py.a.one",
        "version": 1,
        "status": status,
        "title_vi": "Một",
        "est_minutes": 10,
        "objectives_vi": ["a", "b"],
        "blocks": blocks,
        "problems": {"practice": ["add-two"], "extra": []},
        "mastery_check": {"l1": ["Q1"], "l2": ["Q2"], "l3": ["Q3"]},
        "checkpoint": {"pass_ratio": 0.7, "min_items": 3},
    }
    (lessons / "py.a.one.yaml").write_text(yaml.safe_dump(lesson, allow_unicode=True))
    (root / "checks").mkdir()
    checks = {
        "py.a.one": [
            {"id": "Q1", "type": "concept", "minutes": 3, "difficulty": 1, "answer_md": "ans1"},
            {
                "id": "Q2",
                "type": "write_code",
                "minutes": 8,
                "difficulty": 2,
                "prompt_md": "viet add",
                "problem_id": "check-q2",
            },
            {
                "id": "Q3",
                "type": "write_code",
                "minutes": 12,
                "difficulty": 3,
                "prompt_md": "viet add 3",
                "problem_id": "check-q3",
            },
        ],
        # read_code at levels 1-2, a concept level 3 (no write_code => level3_ok is vacuous)
        "py.a.two": [
            {
                "id": "R1",
                "type": "read_code",
                "minutes": 3,
                "difficulty": 1,
                "code": "print(1)",
                "expected_output": "1",
                "answer_md": "one",
            },
            {
                "id": "R2",
                "type": "read_code",
                "minutes": 4,
                "difficulty": 2,
                "code": "print(2)",
                "expected_output": "2",
                "answer_md": "two",
            },
            {"id": "C3", "type": "concept", "minutes": 5, "difficulty": 3, "answer_md": "three"},
        ],
        # only a concept at level 2 and no level 1 item
        "py.a.three": [
            {"id": "C2", "type": "concept", "minutes": 5, "difficulty": 2, "answer_md": "x"},
        ],
    }
    for sid, items in checks.items():
        (root / "checks" / f"{sid}.yaml").write_text(
            yaml.safe_dump({"subtopic_id": sid, "items": items})
        )

    pdir = root / "problems" / "py.a.one" / "add-two"
    (pdir / "tests").mkdir(parents=True)
    problem = {
        "id": "add-two",
        "subtopic_id": "py.a.one",
        "secondary_subtopics": [],
        "kind": "practice",
        "title": "Add Two",
        "title_vi": "Cộng hai",
        "difficulty": "easy",
        "source": {"type": "original"},
        "statement_en_md": "Add.",
        "statement_vi_md": "Cộng.",
        "constraints": [],
        "examples": [{"input": "1 2", "output": "3", "explain_vi": "x"}],
        "io": {
            "mode": "function",
            "entry": "add",
            "params": [],
            "returns": "int",
            "compare": "exact",
        },
        "starter": {"python": "def add(a, b):\n    pass\n"},
        "limits": {"time_ms": 1000, "memory_mb": 256, "time_multiplier": {"pyodide": 3}},
        "time_target_min": 10,
        "hints": ["h1", "h2", "h3"],
        "solution": {"file": "solution.py", "approach_vi": "cộng", "complexity": "O(1)"},
        "tests": {"sample": "tests/sample.jsonl", "hidden": "tests/hidden.jsonl"},
        "tags": [],
        "status": status,
        "version": 1,
    }
    (pdir / "problem.yaml").write_text(yaml.safe_dump(problem, allow_unicode=True))
    (pdir / "solution.py").write_text("def add(a, b):\n    return a + b\n")
    (pdir / "tests" / "sample.jsonl").write_text('{"id":"s1","args":[1,2],"expected":3}\n')
    (pdir / "tests" / "hidden.jsonl").write_text(
        '{"id":"h1","args":[0,0],"expected":0}\n{"id":"h2","args":[5,7],"expected":12}\n'
    )
    for cid, minutes in (("check-q2", 8), ("check-q3", 12)):
        cdir = root / "problems" / "py.a.one" / cid
        (cdir / "tests").mkdir(parents=True)
        cprob = {**problem, "id": cid, "kind": "check", "status": "validated"}
        cprob["time_target_min"] = minutes
        cprob["title"] = cid
        (cdir / "problem.yaml").write_text(yaml.safe_dump(cprob, allow_unicode=True))
        (cdir / "solution.py").write_text("def add(a, b):\n    return a + b  # REFERENCE\n")
        (cdir / "tests" / "sample.jsonl").write_text('{"id":"s1","args":[1,2],"expected":3}\n')
        (cdir / "tests" / "hidden.jsonl").write_text('{"id":"h1","args":[0,0],"expected":0}\n')
    return root


@pytest.fixture
def content_dir(tmp_path: Path) -> Path:
    return build_content(tmp_path / "content")


@pytest.fixture
def draft_content_dir(tmp_path: Path) -> Path:
    return build_content(tmp_path / "draft-content", status="draft")


@pytest.fixture
def clock() -> Clock:
    return Clock()


@pytest.fixture
def settings(tmp_path: Path, content_dir: Path) -> Settings:
    return Settings(
        data_dir=tmp_path / "data",
        content_dir=content_dir,
        backup_dir=None,
        backup_mirror_dir=None,
        serve_drafts=False,
        allow_network_fs=True,  # the sandbox disk may be anything; dedicated tests cover the check
    )


@pytest.fixture
def make_client(settings: Settings, clock: Clock):
    clients: list[TestClient] = []

    def make(**overrides) -> TestClient:
        for k, v in overrides.items():
            setattr(settings, k, v)
        rt = Runtime(settings, clock=clock)
        rt.backup_on_shutdown = False
        c = TestClient(create_app(settings, rt))
        c.__enter__()
        clients.append(c)
        return c

    yield make
    for c in clients:
        c.__exit__(None, None, None)


@pytest.fixture
def client(make_client) -> Iterator[TestClient]:
    yield make_client()
