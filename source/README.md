# Source data

Snapshot of the upstream content the app is built from (copied 2026-10-25 from the project's shared folder, read-only here):

| File | What it is |
|---|---|
| `skill_tree.json` | Layer-1 skill tree: 530 subtopics, prerequisites, Vietnamese explanations |
| `plan.json`, `plan.md` | Meta 30-day intern/new-grad plan (suggested order of subtopics and problems) |
| `assessment.json`, `assessment.md` | 254 assessment items, levels 1-3 (source for mastery checks and placement) |

Regenerate the committed index with:

```
uv run python tools/sync_tree.py source/skill_tree.json source/plan.json
```

Do not edit these files by hand; update them from upstream and re-run the tools.
