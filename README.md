# Prep App

**Vi:** Ứng dụng cá nhân để học lập trình và luyện phỏng vấn: bài học ngắn (lesson), bài tập có
chấm điểm tự động (problem), ôn tập ngắt quãng. Nội dung lấy từ cây kỹ năng và kế hoạch 30 ngày của
Quan; chạy code Python ngay trong trình duyệt. Mới ở mốc M0: khung repo, schema nội dung, bộ
kiểm tra nội dung, 40 lesson nháp và một problem mẫu (`ransom-note`).

**En:** A personal app for learning to code and preparing for interviews: short lessons,
auto-graded problems and spaced review, built from Quan's skill tree and 30-day plan, with Python
running in the browser. This repo is at milestone M0: monorepo skeleton, content schemas, the
content validator, 40 draft lesson stubs and one full sample problem (`ransom-note`).

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
apps/api/      FastAPI skeleton (GET /api/health)
content/       index/ (snapshot of the skill tree and plan, committed), lessons/, problems/,
               schemas/ (JSON Schemas for lesson, problem, check)
tools/         content tooling, run with `uv run python tools/<name>.py`
               sync_tree.py, gen_lesson_stubs.py, gen_hidden.py, run_problem.py, validate_content.py
data/          local SQLite data and backups (git-ignored)
docs/          SPEC.md, UI_SPEC.md
```

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
