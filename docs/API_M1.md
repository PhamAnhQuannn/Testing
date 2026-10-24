# API as implemented in M1

Source of truth for the frontend while M1 is in flight. It follows SPEC 6.4; every difference is
listed under "Deviations" at the end. Code: `apps/api/app/`. Base path `/api`, JSON in and out.

## Conventions

- **Errors**: `{"error": {"code": "...", "message": "...", ...extra}}` with a matching HTTP status.
  Validation failures are `422 validation_error` with `error.details[]`. Unknown routes are
  `404 http_404`.
- **Idempotency**: send `Idempotency-Key: <uuid v4>` on every state-changing POST/PUT. The first
  request runs; repeats with the same key return the stored status and body (plus header
  `Idempotent-Replay: true`) and write nothing. The same key on a different method/path is
  `422 idempotency_key_reuse`; the same key while the first request still runs is
  `409 idempotency_in_progress` (retry in a second). 5xx responses are not stored, so they can be
  retried. The header is optional (no header = no protection). Keys are kept 30 days.
- **A 2xx on a write means the transaction is committed** (WAL, `synchronous=FULL`).
- **Time**: ISO 8601 UTC. Events accept `occurred_at` (client time), clamped to
  `[received - 7 days, received + 5 minutes]`. Review days are `YYYY-MM-DD` in the user's `tz`.
- **User**: fixed (`id = 1`) through `current_user()`; handlers do not take a user id.
- **Content visibility**: only `status: published` lessons/problems are served. With
  `SERVE_DRAFTS=1` (`make dev-api`) drafts are served too and re-read from disk on each request.
- **The server does not enforce locks.** `/map` reports `unlocked`/`lock_reasons`; the UI decides
  whether to disable editor/Submit for a locked subtopic (SPEC 5.3 preview mode).

## Serving the web app

With `WEB_DIST=<apps/web/dist>` (set in the Docker image) FastAPI serves the built app at `/`
(`app/web.py`). Every static response carries the `Content-Security-Policy` header from
`apps/web/vite.config.ts` (the build also writes it to `dist/csp.txt`); worker scripts only honour
the header, not the `<meta>`. `.wasm` is `application/wasm`, `.js`/`.mjs` `text/javascript`.
A GET for a path that is not under `/api` and has no asset extension (`/s/py.datastructs.dict`,
`/p/ransom-note`, `/map`) returns `index.html` so client routes survive a reload; `/api/*` keeps
its JSON `404 http_404`. `assets/*` are cached immutable, everything else `no-cache`.

## Health and durability

### `GET /api/health`
```json
{"status": "ok", "journal_mode": "wal", "synchronous": "2", "schema_version": "0001",
 "last_backup_at": "2026-11-02T03:00:00+00:00"}
```
If the database failed `quick_check` at start: `503 {"status": "db_corrupt", "latest_backup":
"app-....db"}`. In that state every DB-backed route answers `503 db_corrupt`; only `/api/health` and
`/api/backups*` work, so the UI can show a restore screen.

The process refuses to start (exception at startup, non-zero exit) when `PRAGMA journal_mode=WAL`
does not answer `wal`, or the data dir is on nfs/cifs/smb/9p/vboxsf/fuse* (read from
`/proc/mounts`; `ALLOW_NETWORK_FS=1` overrides, tests only).

### Backups
| Request | Response |
|---|---|
| `GET /api/backups` | `{"backups": [{"name": "app-20261102-030000.db", "size": 204800, "created_at": "..."}]}` newest first |
| `POST /api/backups` | `201` one backup object (take one now) |
| `GET /api/backups/{name}` | the file (download) |
| `POST /api/backups/{name}/restore` | `{"status": "ok", "restored": {backup object}}`. Errors: `400 invalid_backup_name`, `404 backup_not_found`, `422 backup_corrupt`, `422 schema_mismatch` |

Restore backs up the current DB first (unless it is damaged, then the file is kept as
`app.db.corrupt-<time>`), checks `integrity_check` and the schema version of the chosen file, loads
it with the SQLite backup API and reopens the app. Reload the page afterwards.
Automatic backups: at start (if the newest is older than 1 h and a DB already existed), before a
migration, every `backup_every_hours` (default 6), and on graceful shutdown. Kept: 20 newest + the
first of each day for 30 days. `BACKUP_DIR` (default `data/backups`) and `BACKUP_MIRROR_DIR`.

## Me and settings

### `GET /api/me`
```json
{"user": {"id": 1, "name": "Quan"},
 "settings": {"tz": "Asia/Ho_Chi_Minh", "review_preset": 6, "backlog_warn": 20, "target_role": null,
   "track": null, "language": null, "experience": null, "display_name": null, "onboarded_at": null,
   "backup_every_hours": 6, "backup_keep": 20, "ui_prefs": {}},
 "onboarding": {"profile_done": false, "placement": "none"},
 "content": {"subtopics": 40, "serve_drafts": true}}
```

### `PUT /api/settings`
Body (all optional): `{"tz": "UTC", "review_preset": 6 | null, "backlog_warn": 20,
"backup_every_hours": 6, "ui_prefs": {"theme": "dark"}}`. Returns the settings object above.
`422 invalid_tz` for an unknown zone.

## Map and content

### `GET /api/map`
```json
{"today": "2026-11-02", "assumed": ["cs.onramp.computer_programming_model"], "due_cards": 0,
 "subtopics": [{
   "id": "py.datastructs.dict", "name_vi": "...", "section": "py", "module": "py.datastructs",
   "order": 9, "plan_day": 3, "est_hours": 2, "target_intern": 2,
   "prerequisites": ["py.datastructs.list"], "content_status": "published", "has_lesson": true,
   "problem_count": 1, "score": 1, "status": "in_progress", "unlocked": false,
   "lock_reasons": [{"prerequisite": "py.datastructs.list", "name_vi": "...", "score": 0, "need": 2}],
   "lesson_done": true, "quiz_best": 0.8, "tested_out": false, "known_basic": false, "due_cards": 0}]}
```
Ordered by plan order. `status`: `locked | unlocked | in_progress | done | blocked_missing_content`.
`content_status`: `none | draft | published` (what the server would serve). A `lock_reasons` entry
for a prerequisite that is neither assumed nor in content has `"missing_content": true`.

### `GET /api/subtopics/{id}`
The map item plus `summary_vi`, `mastery_bar_vi`, `lesson` (`{version, est_minutes, objectives_vi}`
or null), `problems[]` (`{id, title, title_vi, difficulty, kind, role: practice|extra, status:
todo|attempted|solved, solved_clean, attempts}`) and `checks[]` (`{level, item_id, type, minutes}`;
types come from `content/checks/<id>.yaml` when present, otherwise null).

### `GET /api/lessons/{subtopic_id}`
The lesson YAML as JSON (`id, version, status, title_vi, est_minutes, objectives_vi, blocks[],
problems, mastery_check, checkpoint, source`) with secrets removed:
- `code_exercise.solution` is dropped;
- `quiz_mcq`: `answer` and `explain_md` dropped; `quiz_fill`: `blanks` become `[{"index": 0}, ...]`
  and `explain_md` is dropped; `predict_output`: `expected_output` and `explain_md` dropped.
  They come back from `POST /quiz/answers` after the learner answers.

Plus a `progress` object so a reload restores the state:
```json
"progress": {"run_no": 1, "answers": {"b04": {"attempts": 2, "first_correct": false,
  "last_answer": ["b"], "last_correct": true}}, "lesson_done": false, "quiz_best": null,
  "score": 0, "known_basic": false}
```
`answers` covers the current run only. `404 lesson_not_found` when unpublished.

### `POST /api/lessons/{subtopic_id}/runs`  (new pass, "Làm lại lượt")
`201 {"run_no": 2}`. Run 1 exists implicitly.

### `POST /api/quiz/answers`
```json
{"quiz_item_id": "py.datastructs.dict#b04", "run_no": 1, "answer": ["b"], "occurred_at": null}
```
`answer` is a list of option ids (`quiz_mcq`), a list of strings, one per blank (`quiz_fill`,
trimmed, exact match against `accept` or `regex` full match) or a string (`predict_output`,
compared after trimming trailing whitespace per line). Response:
```json
{"correct": true, "attempt_no": 1, "run_no": 1, "first_attempt": true, "graded": true,
 "explain_md": "...", "correct_answer": ["b"], "quiz_best": 0.75}
```
`correct_answer` is `answer[]` / the first `accept` of each blank / `expected_output`.
Only the first answer per block per run counts toward `quiz_best` (later ones get `attempt_no > 1`).
Errors: `404 quiz_item_not_found`, `422 invalid_run | invalid_answer | not_a_quiz`.

### `POST /api/lessons/{subtopic_id}/complete`  (body optional: `{"occurred_at": ...}`)
```json
{"subtopic_id": "py.datastructs.dict", "lesson_done": true, "quiz_best": 0.8, "quiz_passed": true,
 "score": 1, "score_before": 0, "status": "in_progress",
 "review_card": {"box": 1, "due_on": "2026-11-03"}, "newly_unlocked": []}
```
`score` is 1 only when the quiz is also passed (>= 0.7 over >= 3 answered graded blocks);
otherwise 0 and `review_card` is null. Calling it again is harmless (no second event).

## Problems

### `GET /api/problems?subtopic=&difficulty=&status=&kind=`
`{"problems": [{"id", "subtopic_id", "title", "title_vi", "difficulty", "kind", "time_target_min",
"tags", "status": "todo|attempted|solved", "solved_clean", "attempts"}]}`

### `GET /api/problems/{id}`
Public part only: `id, subtopic_id, secondary_subtopics, kind, title, title_vi, difficulty, source,
statement_en_md, statement_vi_md, constraints, examples, io, starter, limits, time_target_min, tags,
version, status`, plus
`sample_tests` (the `sample.jsonl` lines: `{"id","args","expected"}`), `hint_count`, `hints`
(only the ones already opened), `hints_used`, `solution_viewed`, `status`, `solved_clean`,
`attempts`, `last_attempt` (`{mode, verdict, passed, total, at}` or null).
No hidden tests, no solution.

### `POST /api/problems/{id}/hints`
Opens the next hint (max 3). `{"hints_used": 1, "hint": "text of the new hint" | null,
"hints": ["..."], "exhausted": false}`.

### `GET /api/problems/{id}/solution`
Marks `solution_viewed = true` (this makes later attempts not clean).
`{"language": "python", "code": "...", "approach_vi": "...", "complexity": "O(n)"}`.

### Submit flow (hidden tests for the browser runner)
1. `POST /api/problems/{id}/start-submit` -> `{"token": "...", "expires_at": "...", "ttl_s": 900}`.
2. `GET /api/problems/{id}/tests/hidden` with header `X-Submit-Token: <token>` (or `?token=`) ->
   ```json
   {"problem_id": "ransom-note", "problem_version": 1,
    "limits": {"time_ms": 1000, "memory_mb": 256, "time_multiplier": {"pyodide": 3}},
    "tests": [{"id": "h01", "args": ["abc", "ab"], "expected": false, "tags": ["edge"]}]}
   ```
   `403 submit_token_required | submit_token_expired`. The token is valid for 15 minutes and may be
   reused inside that window. Tokens live in memory: a server restart invalidates them.
3. Run the tests in the worker, then `POST /api/attempts`.

### `POST /api/attempts`
```json
{"problem_id": "ransom-note", "mode": "submit", "language": "python", "code": "...",
 "verdict": "AC", "passed": 12, "total": 12, "elapsed_ms": 421000, "runtime_ms": 35,
 "started_at": "2026-11-02T02:50:00Z", "occurred_at": "2026-11-02T03:00:00Z"}
```
`mode` is `run` or `submit`; `verdict` a short string (`AC, WA, TLE, RE, CE, ...`); an `AC` needs
`passed == total` (`422 invalid_counts`). `elapsed_ms` is the cumulative editor time. `started_at`
defaults to the draft's. Response `201`:
```json
{"attempt_id": 7, "verdict": "AC", "ac": true, "clean": true, "hints_used": 0,
 "solution_viewed": false, "elapsed_ms": 421000,
 "score": {"subtopic_id": "py.datastructs.dict", "before": 1, "after": 1, "status": "in_progress",
           "newly_unlocked": []}}
```
`score` is null for `mode: run`. `clean` = submit AC, no solution viewed, `hints_used <= 1` (the
server's count at that moment) and `elapsed_ms <= 1.5 * time_target_min * 60000`. The score is
recomputed from the event tables in the same transaction.

### Drafts
`PUT /api/drafts/{problem_id}`
```json
{"code": "...", "language": "python", "updated_at": "2026-11-02T03:00:02Z",
 "cursor": {"line": 3, "ch": 4}, "elapsed_ms": 61000, "started_at": "2026-11-02T02:59:00Z"}
```
-> `{"accepted": true, "draft": {"problem_id", "language", "code", "updated_at", "cursor",
"elapsed_ms", "started_at", "rev"}}`. The copy with the newer `updated_at` wins; an older one gets
`accepted: false` with the server draft. `elapsed_ms` keeps the max (heartbeats are absolute).
Resending the same code is a no-op. `base_rev` is accepted and ignored in M1.
`GET /api/drafts/{problem_id}?language=python` -> `{"draft": {...} | null}`.

## Resume

`PUT /api/resume` (and `POST /api/resume`, same body, any content type, for `sendBeacon`):
```json
{"mode": "lesson", "route": "/s/py.datastructs.dict",
 "ref": {"subtopic_id": "py.datastructs.dict", "block_id": "b06", "scroll_in_block": 0.4, "tab": "lesson"},
 "context": {}, "device_id": "d1", "updated_at": "2026-11-02T03:00:00Z"}
```
`mode`: `lesson | problem | check | placement | review | other`. An older `updated_at` never
overwrites a newer stored position. -> `{"ok": true}`.

`GET /api/resume`
```json
{"primary": {"mode": "lesson", "route": "/s/...", "ref": {}, "context": {}, "updated_at": "...",
             "device_id": "d1", "stale": false},
 "others": [{"mode": "lesson", "route": "/s/dsa.arrays_strings.arrays",
             "ref": {"subtopic_id": "..."}, "name_vi": "..."}],
 "in_progress": {"placement": null, "check": null, "review": null}}
```
`primary` is null when nothing was saved. `stale` is true when the lesson's subtopic is `done` or the
problem was AC'd after the position was saved. `others` = up to 3 other `in_progress` subtopics.

## Deviations from SPEC 6.4

1. **Not implemented in M1** (later milestones): `PUT /profile`, placement, checks, review,
   `/next`, `/activity/ping`, `/stats`, `/feedback`, `/export`, `/import`, `/reset`.
   `GET /me` returns `onboarding.placement: "none"` always.
2. **Added**: `GET /drafts/{problem_id}` (needed to load a draft), `POST /resume` (beacon),
   `PUT /settings` accepts `backup_every_hours` and `ui_prefs`, a `progress` object in
   `GET /lessons/{id}`, `last_attempt` in `GET /problems/{id}`.
3. **Hidden tests**: `GET /problems/{id}/tests/hidden` takes the token as `X-Submit-Token` header or
   `?token=`; tokens are in memory (a restart invalidates them).
4. **Quiz secrets stay on the server** (the lesson JSON has no answers/explanations); see above.
   This is how 6.4 reads (`POST /quiz/answers` returns `correct` + `explain_md`), spelled out here.
5. **`problem_state` table** (`hints_used`, `solution_viewed`, `first_opened_at`) holds what 6.3 does
   not place anywhere; `check_results.item_type` and a `lesson_runs` table are also additions.
6. **Drafts**: M1 behaviour (newer `updated_at` wins, no 409, `rev` only informative).
7. **Locks are not enforced server side** (the UI decides), so the M1 acceptance flow (learn
   `py.datastructs.dict` end to end) is possible even while its prerequisites are at score 0.
8. **Check items** (for `has_l3_write_code` and `item_type`) are read from
   `content/checks/<subtopic_id>.yaml` (SPEC 3.1). Without that file `level3_ok` falls back to the
   medium-practice rule, then to true (SPEC 5.2).
9. `GET /health` returns `status, journal_mode, synchronous, schema_version, last_backup_at`;
   `503` with `status: db_corrupt` when the DB is damaged.
10. Idempotency: the stored response is replayed as JSON (same data, not byte-identical).
