.PHONY: install lint test validate validate-public web-build ci sync-tree stubs dev-api backup

WEB := apps/web

# Everything CI runs, in the same order: `make ci` on a fresh clone must end green.
ci: install lint test validate web-build

install:
	uv sync --locked --all-packages
	cd $(WEB) && npm ci
	cd tools/pyodide-node && npm ci

lint:
	uv run ruff check .
	uv run ruff format --check .
	cd $(WEB) && npm run lint

test:
	uv run pytest

# Native checks plus the stress tests under Pyodide in Node (tools/pyodide-node).
validate:
	uv run python tools/validate_content.py --pyodide

# The public-bundle gate: fails while a published problem still has rewrite_required.
# Not part of `ci`; run it before building a bundle anyone else can read.
validate-public:
	uv run python tools/validate_content.py --pyodide --public

web-build:
	cd $(WEB) && npm run build

# Refresh content/index/ from the source data, e.g.
#   make sync-tree TREE=/path/skill_tree.json PLAN=/path/plan.json
sync-tree:
	uv run python tools/sync_tree.py $(TREE) $(PLAN)

# Create draft lesson stubs for subtopics that have no lesson file yet.
stubs:
	uv run python tools/gen_lesson_stubs.py

# API on 127.0.0.1:8000 with the draft lessons/problems served too (dev). Data in ./data/app.db.
dev-api:
	cd apps/api && SERVE_DRAFTS=1 uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Take a backup now through the running API (docker compose or dev-api).
backup:
	curl -fsS -X POST http://127.0.0.1:$${PORT:-8080}/api/backups
