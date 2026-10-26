# Prep App

**Vi:** Ứng dụng cá nhân để học lập trình và luyện phỏng vấn: bài học ngắn (lesson), bài tập có
chấm điểm tự động (problem), ôn tập ngắt quãng. Nội dung lấy từ cây kỹ năng và kế hoạch 30 ngày của
Quan; chạy code Python ngay trong trình duyệt. **Đã xong M2a**: vòng lặp học đầy đủ — onboarding +
placement, "Học tiếp", lesson + editor, mastery check / Test out, điểm 0-3, mở khoá + skill map,
ôn lặp Leitner, backup/khôi phục, tiếp tục sau khi thoát; 17 lesson và 89 problem đã publish (16 mục
ngày 1-3 của kế hoạch). Dữ liệu nguồn ở [source/](source/README.md). Chạy: `docker compose up` rồi
mở http://127.0.0.1:8080.

**En:** A personal app for learning to code and preparing for interviews: short lessons,
auto-graded problems and spaced review, built from Quan's skill tree and 30-day plan, with Python
running in the browser. **Milestone M2a is done**: the full learning loop — onboarding + placement,
a "Continue" home, lesson + editor, mastery check / Test out, 0-3 scoring, prerequisite unlock +
skill map, Leitner spaced review, backup/restore, and resume-after-exit; 17 lessons and 89 problems
are published (the 16 days-1-3 plan subtopics). Upstream source data is in
[source/](source/README.md). Run: `docker compose up`, then open http://127.0.0.1:8080.

Full specification: [docs/SPEC.md](docs/SPEC.md) (Vietnamese), screens in
[docs/UI_SPEC.md](docs/UI_SPEC.md).

## Run `make ci`

Needs [uv](https://docs.astral.sh/uv/) (it fetches Python 3.12), Node 22.12+ and npm. Linux or
macOS: `tools/run_problem.py` watches its child process with `select` on a pipe, which does not
work on Windows (use WSL).

```sh
make ci
```

It installs the locked dependencies, then runs the same steps as
[`.github/workflows/ci.yml`](.github/workflows/ci.yml): `lint` (ruff, eslint), `test` (pytest for
`tools/` and `apps/api/`), `validate` (`tools/validate_content.py`) and `web-build`
(type-check and Vite build). Each step is also its own target, e.g. `make validate`.

## Layout

```
apps/web/      Vite + React + TypeScript skeleton
               src/runner/pyodide/harness.py is the one test harness, shared by the browser
               worker (M1) and tools/run_problem.py
apps/api/      FastAPI + SQLite (SQLAlchemy, Alembic): see docs/API_M1.md; `make dev-api`, `docker compose up`
content/       index/ (snapshot of the skill tree and plan, committed), lessons/, problems/,
               schemas/ (JSON Schemas for lesson, problem, check)
tools/         content tooling, run with `uv run python tools/<name>.py`
               sync_tree.py, gen_lesson_stubs.py, gen_hidden.py, run_problem.py, validate_content.py
data/          local SQLite data and backups (git-ignored)
docs/          SPEC.md, UI_SPEC.md, API_M1.md, OVERVIEW.md, NEXT_M2A.md
```

## Làm việc với VS Code + Claude Code

Mở thư mục repo trong VS Code (chấp nhận extension gợi ý trong `.vscode/extensions.json`), chạy
`make install` rồi `make ci`, sau đó mở Claude Code ở thư mục gốc: nó tự đọc [CLAUDE.md](CLAUDE.md)
(quy tắc, lệnh, quy ước, gotchas). M2a đã xong (xem [docs/NEXT_M2A.md](docs/NEXT_M2A.md) cho các task
đã làm); việc tiếp theo là M2b (SPEC §7: hết tuần 1 — 12 mục ngày 4-7, `/problems` + `/progress` +
export/import, placement đầy đủ Phase B/C). Tổng quan yêu cầu và hiện trạng ở
[docs/OVERVIEW.md](docs/OVERVIEW.md).

## End-to-end check (real API)

`make e2e` builds the web app, starts uvicorn on a temp SQLite dir and drives Chromium through the
SPEC 7 M1 acceptance (lesson, quiz, exercise, Submit AC, score, reload, TLE, kill -9, idempotency,
backup restore). Needs `make install` and `playwright` resolvable by `require()` (`NODE_PATH`).

## Content tooling

```sh
# Refresh content/index/ (CI cannot read the source files, so the result is committed):
make sync-tree TREE=<skill_tree.json> PLAN=<plan.json>

# Regenerate a problem's hidden tests, then run a solution (or a wrong/slow one) against them:
uv run python tools/gen_hidden.py content/problems/py.datastructs.dict/ransom-note
uv run python tools/run_problem.py content/problems/py.datastructs.dict/ransom-note \
    --solution wrong/no_count.py

# Check all content:
make validate
```
