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
from .concepts import registry_of
from .scoring import SubtopicSpec

GRADED_TYPES = {"quiz_mcq", "quiz_fill", "predict_output"}

# Concept tracks (SPEC 5.2): System Design and the AI-engineer LLM subset of `ml`. A subtopic of
# one of these with no code evidence is a "concept subtopic" (see `spec_for`). Must match the
# selection in tools/sync_tree.py.
CONCEPT_SECTIONS = {"sd"}
CONCEPT_MODULES = {"ml.llm", "ml.rag_agents", "ml.llm_eval_serving", "ml.system_design"}


# Role model: the knowledge tree's 4 levels and the 2 role tracks. The chosen level selects the
# readiness `target` ONLY (SPEC 5.7); it never feeds score, unlock, Leitner or /next.
LEVELS = ("intern", "fresher", "junior", "senior")
ROLE_TRACKS = ("swe", "ai")
LEGACY_LEVELS = {"new_grad": "fresher"}  # pre-4-level settings / links still resolve


# Domain config: the single authority for tracks, section and module labels. GET /diagnosis serves
# it so the web does not duplicate it.
TRACKS: list[dict[str, Any]] = [
    {"key": "foundation", "name_vi": "Nền tảng", "sections": ["py", "cs", "dsa"]},
    {"key": "system_design", "name_vi": "System Design", "sections": ["sd"]},
    {"key": "ai", "name_vi": "AI engineer (LLM)", "sections": ["ml"]},
]
SECTION_NAMES: dict[str, str] = {
    "py": "Python nền tảng",
    "cs": "Độ phức tạp & CS",
    "dsa": "Thuật toán & CTDL (DSA)",
    "sd": "System Design",
    "ml": "AI engineer (LLM)",
}
MODULE_NAMES: dict[str, str] = {
    "py.core": "Cốt lõi Python",
    "py.datastructs": "Cấu trúc dữ liệu Python",
    "py.functions": "Hàm",
    "py.oop": "Hướng đối tượng",
    "cs.complexity": "Độ phức tạp",
    "dsa.foundations": "Nền tảng DSA",
    "dsa.arrays_strings": "Mảng & chuỗi",
    "dsa.two_pointers_window": "Hai con trỏ & cửa sổ trượt",
    "dsa.linked_list": "Danh sách liên kết",
    "dsa.stack_queue": "Ngăn xếp & hàng đợi",
    "dsa.recursion_backtracking": "Đệ quy & quay lui",
    "dsa.searching_sorting": "Tìm kiếm & sắp xếp",
    "dsa.trees": "Cây",
    "sd.fundamentals": "Nền tảng thiết kế hệ thống",
    "sd.networking": "Mạng",
    "sd.api": "Thiết kế API",
    "sd.data": "Dữ liệu & lưu trữ",
    "sd.caching": "Cache",
    "sd.async": "Bất đồng bộ & hàng đợi",
    "sd.distributed": "Hệ phân tán",
    "sd.reliability_ops": "Độ tin cậy & vận hành",
    "sd.framework": "Khung thiết kế",
    "sd.technologies": "Công nghệ thường gặp",
    "sd.archetypes": "Bài toán thiết kế mẫu",
    "ml.llm": "LLM cơ bản",
    "ml.rag_agents": "RAG & agent",
    "ml.llm_eval_serving": "Đánh giá & triển khai LLM",
    "ml.system_design": "Thiết kế hệ thống AI",
}


def module_name(module_id: str) -> str:
    """Vietnamese label of a module, or a prettified fallback from its last dotted segment."""
    known = MODULE_NAMES.get(module_id)
    if known:
        return known
    return module_id.rsplit(".", 1)[-1].replace("_", " ").capitalize()


def track_of(section: str) -> str:
    """Key of the track a section belongs to ("other" if none)."""
    for tr in TRACKS:
        if section in tr["sections"]:
            return tr["key"]
    return "other"


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
    # Placement-only items (mcq / read_code rungs), kept OUT of `checks` so that spec_for and the
    # mastery item selectors never see them. Resolved for grading by `find_check_item`.
    placement: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
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

        self.placement = {}
        for path in sorted((root / "placement").glob("*.yaml")):
            data = _load_yaml(path)
            if isinstance(data, dict) and "items" in data:
                self.placement[data["subtopic_id"]] = data["items"]

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
        all_items = self.checks.get(subtopic_id, [])
        # Concept subtopic (SPEC 5.2): a subtopic of a concept TRACK (System Design + the
        # AI-engineer LLM track) that has no code evidence path (no practice, no write_code item).
        # Gating on the track matters: a py/dsa/cs subtopic that merely lacks a write_code item
        # while being authored must NOT become concept (its score-2 bar stays measured code). A
        # concept-track subtopic that DOES carry code (e.g. a rate-limiter exercise) is not concept
        # either and uses the normal code path. has_l3_items gates the concept level-3 pass.
        node = self.subtopics.get(subtopic_id, {})
        in_concept_track = (
            node.get("section") in CONCEPT_SECTIONS or node.get("module") in CONCEPT_MODULES
        )
        has_code = bool(practice) or any(i.get("type") == "write_code" for i in all_items)
        is_concept = in_concept_track and not has_code
        has_l3_items = any(i.get("difficulty") == 3 for i in all_items)
        return SubtopicSpec(
            practice_ids=practice,
            medium_practice_ids=medium,
            graded_quiz_ids=graded,
            has_l2_items=l2,
            has_l3_write_code=l3,
            is_concept=is_concept,
            has_l3_items=has_l3_items,
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

    def curated_check_items(self, subtopic_id: str) -> dict[int, list[dict[str, Any]]]:
        """`check_items` narrowed to the lesson's `mastery_check` (SPEC 3.5) per level.

        A level whose `mastery_check` list is empty or missing, or names no existing item of that
        level, keeps all of its items (hand-written / not-yet-authored lessons)."""
        out = self.check_items(subtopic_id)
        lesson = self.lessons.get(subtopic_id)
        mc = (lesson.data.get("mastery_check") or {}) if lesson else {}
        for level in (1, 2, 3):
            named = mc.get(f"l{level}") or []
            picked = [i for i in out[level] if i["id"] in named]
            if picked:
                out[level] = picked
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

    def find_check_item(self, subtopic_id: str, item_id: str) -> dict[str, Any] | None:
        """A check item by id: the mastery pool first, then the placement-only pool."""
        for pool in (self.checks, self.placement):
            for i in pool.get(subtopic_id, []):
                if i["id"] == item_id:
                    return i
        return None

    def concept_registry(self, subtopic_id: str) -> dict[str, str]:
        """{slug: text} of the subtopic's index concepts (the valid item `concepts` tags)."""
        return registry_of(self.subtopics.get(subtopic_id) or {})

    def item_concepts(self, subtopic_id: str, item_id: str) -> list[str]:
        """Concept slugs an item is tagged with; unknown slugs are ignored defensively."""
        item = self.find_check_item(subtopic_id, item_id)
        if not item:
            return []
        registry = self.concept_registry(subtopic_id)
        return [c for c in item.get("concepts") or [] if c in registry]

    def check_item_type(self, subtopic_id: str, item_id: str) -> str:
        item = self.find_check_item(subtopic_id, item_id)
        return item["type"] if item else "write_code"

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
        if d.get("item_kind") == "write_test":
            # write_test (SPEC 5.7): the client runs the learner's test against the buggy and the
            # correct implementation itself, so both sources are served. The hidden-test token flow
            # is not used. These are not secrets: the learner is shown the buggy code anyway, and
            # `reference_code` is only a correct implementation to run the learner's test against.
            out["item_kind"] = "write_test"
            out["buggy_code"] = self._read_text(e.dir / "buggy.py")
            out["reference_code"] = self._read_text(e.dir / "solution.py")
            out["starter_test"] = (d.get("starter") or {}).get("python", "")
        return out

    @staticmethod
    def _read_text(path: Path) -> str:
        return path.read_text(encoding="utf-8") if path.exists() else ""

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
            prow.difficulty = pe.data.get("difficulty", "medium")  # write_test: none
            prow.source_type = src.get("type", "original")
            prow.lc = src.get("lc")
            prow.time_target_min = pe.data.get("time_target_min", 8)
            prow.path = str(pe.dir.relative_to(self.root))
            prow.content_hash = pe.content_hash
            session.merge(prow)
        session.flush()

    def problem_version(self, session: Session, problem_id: str) -> int:
        row = session.scalar(select(t.Problem.version).where(t.Problem.id == problem_id))
        return row or 1
