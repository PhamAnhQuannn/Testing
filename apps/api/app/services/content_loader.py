"""Reads content/ (SPEC 6.6): the index, lessons, problems and check items.

Lessons and problems are served from the files; only a summary is mirrored into the DB (by
`sync_db`), keyed by `content_hash`. Only `published` content is public; `serve_drafts` (dev) also
serves the rest.
"""

from __future__ import annotations

import copy
import hashlib
import json
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import tables as t
from .scoring import SubtopicSpec

GRADED_TYPES = {"quiz_mcq", "quiz_fill", "predict_output"}


def _hash(*paths: Path) -> str:
    h = hashlib.sha256()
    for p in paths:
        h.update(p.read_bytes())
    return h.hexdigest()


def _load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


@dataclass
class LessonEntry:
    id: str
    path: Path
    data: dict[str, Any]
    content_hash: str

    @property
    def status(self) -> str:
        return self.data.get("status", "draft")

    def graded_ids(self) -> list[str]:
        return [
            f"{self.id}#{b['id']}"
            for b in self.data.get("blocks", [])
            if b["type"] in GRADED_TYPES and b.get("graded", True)
        ]

    def block(self, block_id: str) -> dict[str, Any] | None:
        return next((b for b in self.data.get("blocks", []) if b["id"] == block_id), None)


@dataclass
class ProblemEntry:
    id: str
    dir: Path
    data: dict[str, Any]
    content_hash: str

    @property
    def status(self) -> str:
        return self.data.get("status", "draft")

    @property
    def subtopic_id(self) -> str:
        return self.data["subtopic_id"]


@dataclass
class ContentStore:
    root: Path
    serve_drafts: bool = False
    subtopics: dict[str, dict[str, Any]] = field(default_factory=dict)
    assumed: set[str] = field(default_factory=set)
    plan_days: list[dict[str, Any]] = field(default_factory=list)
    lessons: dict[str, LessonEntry] = field(default_factory=dict)
    problems: dict[str, ProblemEntry] = field(default_factory=dict)
    checks: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    sort_key: dict[str, tuple[int, int]] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    # ---- loading ----

    @classmethod
    def load(cls, root: Path, serve_drafts: bool = False) -> ContentStore:
        store = cls(root=root, serve_drafts=serve_drafts)
        store.reload()
        return store

    def reload(self) -> None:
        root = self.root
        idx = root / "index"
        subs = json.loads((idx / "subtopics.json").read_text(encoding="utf-8"))["subtopics"]
        self.subtopics = {s["id"]: s for s in subs}
        assumed = idx / "assumed.json"
        self.assumed = (
            set(json.loads(assumed.read_text(encoding="utf-8"))["assumed"])
            if assumed.exists()
            else set()
        )
        plan = idx / "plan.json"
        self.plan_days = (
            json.loads(plan.read_text(encoding="utf-8"))["days"] if plan.exists() else []
        )
        self.sort_key = {}
        for day in self.plan_days:
            for pos, s in enumerate(day.get("subtopics", [])):
                self.sort_key.setdefault(s["id"], (day["day"], pos))
        for s in subs:
            self.sort_key.setdefault(s["id"], (10_000, s.get("order", 0)))

        self.lessons = {}
        for path in sorted((root / "lessons").glob("**/*.yaml")):
            data = _load_yaml(path)
            if isinstance(data, dict) and data.get("id") in self.subtopics:
                self.lessons[data["id"]] = LessonEntry(data["id"], path, data, _hash(path))

        self.problems = {}
        for pyaml in sorted((root / "problems").glob("*/*/problem.yaml")):
            data = _load_yaml(pyaml)
            if isinstance(data, dict) and data.get("id"):
                self.problems[data["id"]] = ProblemEntry(
                    data["id"], pyaml.parent, data, _hash(pyaml)
                )

        self.checks = {}
        for path in sorted((root / "checks").glob("*.yaml")):
            data = _load_yaml(path)
            if isinstance(data, dict) and "items" in data:
                self.checks[data["subtopic_id"]] = data["items"]

    # ---- visibility ----

    def _visible(self, status: str) -> bool:
        return self.serve_drafts or status == "published"

    def lesson(self, subtopic_id: str) -> LessonEntry | None:
        e = self.lessons.get(subtopic_id)
        if e is None or not self._visible(e.status):
            return None
        if self.serve_drafts:  # dev: pick up edits without a restart
            try:
                e.data = _load_yaml(e.path)
                e.content_hash = _hash(e.path)
            except OSError:
                return None
        return e

    def problem(self, problem_id: str) -> ProblemEntry | None:
        e = self.problems.get(problem_id)
        if e is None or not self._visible(e.status):
            return None
        if self.serve_drafts:
            p = e.dir / "problem.yaml"
            e.data = _load_yaml(p)
            e.content_hash = _hash(p)
        return e

    def content_status(self, subtopic_id: str) -> str:
        e = self.lessons.get(subtopic_id)
        if e is None:
            return "none"
        return e.status if self._visible(e.status) else "none"

    def problems_of(self, subtopic_id: str) -> list[ProblemEntry]:
        return [
            p
            for p in self.problems.values()
            if p.subtopic_id == subtopic_id and self._visible(p.status)
        ]

    def ordered_subtopic_ids(self) -> list[str]:
        return sorted(self.subtopics, key=lambda i: self.sort_key[i])

    # ---- facts for scoring ----

    def spec_for(self, subtopic_id: str) -> SubtopicSpec:
        lesson = self.lessons.get(subtopic_id)
        practice: tuple[str, ...] = ()
        pass_ratio, min_items = 0.7, 3
        graded: tuple[str, ...] = ()
        l2 = l3 = False
        if lesson:
            d = lesson.data
            practice = tuple(d.get("problems", {}).get("practice", []))
            cp = d.get("checkpoint") or {}
            pass_ratio = cp.get("pass_ratio", pass_ratio)
            min_items = cp.get("min_items", min_items)
            graded = tuple(lesson.graded_ids())
            mc = d.get("mastery_check") or {}
            items = {i["id"]: i for i in self.checks.get(subtopic_id, [])}
            l2 = bool(mc.get("l2"))
            l3 = any(items.get(i, {}).get("type") == "write_code" for i in mc.get("l3") or [])
        # content/checks is the authority for which items exist (the lesson's `mastery_check` lists
        # may be empty in hand-written lessons). Without this, a subtopic that has check items but
        # an empty list would fall back to "one clean practice AC = score 2" (the M1 D1 fallback).
        for item in self.checks.get(subtopic_id, []):
            if item.get("difficulty") == 2:
                l2 = True
            if item.get("difficulty") == 3 and item.get("type") == "write_code":
                l3 = True
        medium = tuple(
            p
            for p in practice
            if p in self.problems and self.problems[p].data.get("difficulty") == "medium"
        )
        return SubtopicSpec(
            practice_ids=practice,
            medium_practice_ids=medium,
            graded_quiz_ids=graded,
            has_l2_items=l2,
            has_l3_write_code=l3,
            pass_ratio=pass_ratio,
            min_items=min_items,
        )

    def check_items(self, subtopic_id: str) -> dict[int, list[dict[str, Any]]]:
        """Check items of a subtopic by level (= item difficulty 1-3), file order kept."""
        out: dict[int, list[dict[str, Any]]] = {1: [], 2: [], 3: []}
        for i in self.checks.get(subtopic_id, []):
            if i.get("difficulty") in out:
                out[i["difficulty"]].append(i)
        return out

    def check_problem(self, problem_id: str) -> ProblemEntry | None:
        """A `kind: check` problem, served to the check flow whatever its publication status."""
        e = self.problems.get(problem_id)
        if e is None or e.data.get("kind") != "check":
            return None
        if self.serve_drafts:
            p = e.dir / "problem.yaml"
            e.data = _load_yaml(p)
            e.content_hash = _hash(p)
        return e

    def check_item_of_problem(self, problem_id: str) -> tuple[str, dict[str, Any]] | None:
        for sid, items in self.checks.items():
            for i in items:
                if i.get("problem_id") == problem_id:
                    return sid, i
        return None

    def check_item_type(self, subtopic_id: str, item_id: str) -> str:
        for i in self.checks.get(subtopic_id, []):
            if i["id"] == item_id:
                return i["type"]
        return "write_code"

    # ---- public views ----

    def public_lesson(self, e: LessonEntry) -> dict[str, Any]:
        """The lesson as served: no `solution`, and quiz answers stay on the server (graded by
        POST /quiz/answers)."""
        d = copy.deepcopy(e.data)
        for b in d.get("blocks", []):
            t_ = b["type"]
            if t_ == "code_exercise":
                b.pop("solution", None)
            elif t_ == "quiz_mcq":
                b.pop("answer", None)
                b.pop("explain_md", None)
            elif t_ == "quiz_fill":
                b.pop("explain_md", None)
                b["blanks"] = [{"index": i} for i, _ in enumerate(b.get("blanks", []))]
            elif t_ == "predict_output":
                b.pop("expected_output", None)
                b.pop("explain_md", None)
        return d

    def public_problem(self, e: ProblemEntry) -> dict[str, Any]:
        d = e.data
        keys = [
            "id",
            "subtopic_id",
            "secondary_subtopics",
            "kind",
            "title",
            "title_vi",
            "difficulty",
            "source",
            "statement_en_md",
            "statement_vi_md",
            "constraints",
            "examples",
            "io",
            "starter",
            "limits",
            "time_target_min",
            "tags",
            "version",
            "status",
        ]
        out = {k: copy.deepcopy(d[k]) for k in keys if k in d}
        out["sample_tests"] = self.sample_tests(e)
        out["hint_count"] = len(d.get("hints", []))
        return out

    def sample_tests(self, e: ProblemEntry) -> list[dict[str, Any]]:
        rel = e.data.get("tests", {}).get("sample")
        p = e.dir / rel if rel else e.dir / "tests" / "sample.jsonl"
        return _read_jsonl(p) if p.exists() else []

    def hidden_tests(self, e: ProblemEntry) -> list[dict[str, Any]]:
        rel = e.data.get("tests", {}).get("hidden")
        p = e.dir / rel if rel else e.dir / "tests" / "hidden.jsonl"
        return _read_jsonl(p) if p.exists() else []

    def solution(self, e: ProblemEntry) -> dict[str, Any]:
        sol = e.data.get("solution", {})
        f = e.dir / sol.get("file", "solution.py")
        return {
            "language": "python",
            "code": f.read_text(encoding="utf-8") if f.exists() else "",
            "approach_vi": sol.get("approach_vi"),
            "complexity": sol.get("complexity"),
        }

    # ---- DB mirror ----

    def sync_db(self, session: Session) -> None:
        """Upsert the content tables by content_hash. Lessons/problems stay served from files."""
        for sid, s in self.subtopics.items():
            tgt = s.get("target_swe", {}) or {}
            tai = s.get("target_ai", {}) or {}
            row = session.get(t.Subtopic, sid) or t.Subtopic(id=sid)
            row.name_vi = s["name_vi"]
            row.section = s["section"]
            row.module = s["module"]
            row.ord = self.sort_key[sid][0] * 1000 + self.sort_key[sid][1]
            row.prereqs = s.get("prerequisites", [])
            row.target_intern = tgt.get("intern", 0)
            row.target_ai = tai.get("intern", 0)
            row.targets = {"swe": tgt, "ai": tai}
            row.est_hours = s.get("est_hours", 0)
            row.summary_vi = s.get("summary_vi", "")
            row.mastery_bar_vi = s.get("mastery_bar_vi", "")
            row.content_status = self.content_status(sid)
            session.merge(row)
        session.flush()

        for sid, le in self.lessons.items():
            lrow = session.get(t.Lesson, sid) or t.Lesson(subtopic_id=sid)
            lrow.version = le.data.get("version", 1)
            lrow.path = str(le.path.relative_to(self.root))
            lrow.content_hash = le.content_hash
            lrow.est_minutes = le.data.get("est_minutes", 0)
            session.merge(lrow)
            seen = set()
            for b in le.data.get("blocks", []):
                if b["type"] in GRADED_TYPES:
                    qid = f"{sid}#{b['id']}"
                    seen.add(qid)
                    session.merge(
                        t.QuizItem(
                            id=qid,
                            subtopic_id=sid,
                            source="lesson",
                            level=None,
                            type=b["type"],
                            graded=b.get("graded", True),
                        )
                    )
        for pid, pe in self.problems.items():
            if pe.subtopic_id not in self.subtopics:
                continue
            prow = session.get(t.Problem, pid)
            src = pe.data.get("source", {})
            if prow is None:
                prow = t.Problem(id=pid, version=1)
            elif prow.content_hash != pe.content_hash:
                prow.version += 1  # attempts keep the version they were made against
            prow.subtopic_id = pe.subtopic_id
            prow.kind = pe.data.get("kind", "practice")
            prow.title = pe.data["title"]
            prow.difficulty = pe.data["difficulty"]
            prow.source_type = src.get("type", "original")
            prow.lc = src.get("lc")
            prow.time_target_min = pe.data["time_target_min"]
            prow.path = str(pe.dir.relative_to(self.root))
            prow.content_hash = pe.content_hash
            session.merge(prow)
        session.flush()

    def problem_version(self, session: Session, problem_id: str) -> int:
        row = session.scalar(select(t.Problem.version).where(t.Problem.id == problem_id))
        return row or 1
