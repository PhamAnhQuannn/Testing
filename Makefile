.PHONY: install lint test validate web-build ci sync-tree stubs

WEB := apps/web

# Everything CI runs, in the same order: `make ci` on a fresh clone must end green.
ci: install lint test validate web-build

install:
	uv sync --locked --all-packages
	cd $(WEB) && npm ci

lint:
	uv run ruff check .
	uv run ruff format --check .
	cd $(WEB) && npm run lint

test:
	uv run pytest

validate:
	uv run python tools/validate_content.py

web-build:
	cd $(WEB) && npm run build

# Refresh content/index/ from the source data, e.g.
#   make sync-tree TREE=/path/skill_tree.json PLAN=/path/plan.json
sync-tree:
	uv run python tools/sync_tree.py $(TREE) $(PLAN)

# Create draft lesson stubs for subtopics that have no lesson file yet.
stubs:
	uv run python tools/gen_lesson_stubs.py
