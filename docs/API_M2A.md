# API additions in M2a

Extends [API_M1.md](API_M1.md) (conventions, errors, idempotency are unchanged). Code:
`apps/api/app/routers/checks.py`, `apps/api/app/services/checks.py`.

## Mastery check and test out (T2.2b, SPEC flows C and D)

Paths follow SPEC 6.4 (`UI_SPEC.md` S8 writes `/checks/{session}/answer`; the SPEC wins, the session
id travels in the body). Table `check_sessions` (migration `0002`); results are appended to
`check_results` (which already had `attempt_no`, `session_id`, `context`, `gave_up`), and the score
is recomputed by `scoring.score` after every result. All three POSTs honour `Idempotency-Key`.

### `POST /api/checks/{subtopic_id}/start`

Body (optional): `{"context": "mastery" | "test_out"}` (default `mastery`; Test out is the same flow,
the context is only recorded). Starts a check or resumes the in-progress session (idle < 24 h,
`resumed: true`). An idle session of 24 h or more becomes `expired` (not a failure).

```
{ session_id, subtopic_id, context, attempt_no, status, resumed, elapsed_ms, started_at, expires_at,
  step: { index, count, item_id, level, type, minutes, time_limit_ms, prompt_md,
          problem_id (write_code) | code (read_code) | answer_md (concept) },
  results: [ {item_id, level, passed, clean, gave_up, ...} ] }
```

The item never carries `reference`, `expected_output` or the rubric. A `write_code` item is a
`kind: check` problem: load it with `GET /problems/{problem_id}` (served even though its status is
`validated`), open hints with `POST /problems/{id}/hints`, run the hidden tests in the browser like
Submit. `GET /problems/{id}/solution` of a check problem is `403 check_solution_locked` until the
item is passed. A new session resets `hints_used` / `solution_viewed` of the subtopic's check problems.

Errors: `404 subtopic_not_found`, `404 check_not_found` (no level 2 item),
`409 check_retry_locked` with `error.retry_after` (ISO time) and `error.level`,
`409 check_already_passed` (level 2 and every level 3 `write_code` already passed).

### `POST /api/checks/{subtopic_id}/answer`

One item result; advances the ladder. Body: `session_id`, `item_id` (must be the current item),
`elapsed_ms` (editor time on this item), optional `session_elapsed_ms`, and per type:

| type | fields | grading |
|---|---|---|
| `write_code` | `code`, `verdict`, `passed_tests`, `total` (+ `language`, `runtime_ms`) | browser ran the hidden tests; the server records an `attempts` row and decides `clean` |
| `read_code` | `answer` (predicted output) | server compares with `expected_output` (trailing whitespace ignored) |
| `concept` | `self_grade` (bool) | self-graded; stored `clean = false`, so never evidence for score 2/3 |
| any | `gave_up: true` | "Khong biet": `passed=false, gave_up=true`; no lock, not a failure for the exit rule |

`passed` = correct for `write_code` / `read_code` (AC / expected output). `clean` is separate: correct
AND no solution view, <= 1 hint, `elapsed_ms <= 1.5 x minutes` (SPEC 5.1). A correct but unclean
answer is `correct = true, passed = true, clean = false` with `reason` = `hint_limit` |
`solution_viewed` | `over_time`: the ladder goes on, no lock starts, but it is not evidence (only
`passed AND clean` counts for tested_out / score 2 / 3).

Ladder (keys on correctness): level 2 (write_code preferred; a redo rotates through same-type items)
-> correct, clean or not: level 3 if the subtopic has one; wrong answer or give up: level 1 as a
diagnostic (none: `outcome.need_lesson = true`).
Level 1 never changes the score. A subtopic whose level 2 is already passed starts at level 3.

```
{ session_id, status, finished,
  result: { item_id, level, type, correct, passed, clean, gave_up, reason?, verdict?, tests_passed?, tests_total? },
  next: { index, count, ...item } | null,
  score: { subtopic_id, before, after, status, tested_out, newly_unlocked[] },
  outcome: null | { level1, level2, level3 ("passed"|"failed"|"gave_up"|null), tested_out, score,
                    need_lesson, retry_after, newly_unlocked[] } }
```

A fail never includes the reference. Errors: `404 check_session_not_found`,
`409 check_session_expired | check_session_done | check_wrong_item | check_item_answered`,
`422 missing_field | invalid_counts`.

### `POST /api/checks/{session_id}/heartbeat`

Body `{"elapsed_ms": <absolute active time>}`; keeps the session alive (resets the 24 h idle clock)
and stores the max `elapsed_ms`, so a resend is safe. Returns `{session_id, status, elapsed_ms,
expires_at}`. `409 check_session_expired`, `404 check_session_not_found`.

### Rules in one place

- Redo after a failed level only after 24 h (`passed = false AND gave_up = false`, i.e. a real wrong
  answer; any context, per level). A correct-but-unclean answer never starts a lock. Each session is
  a new `attempt_no`.
- `tested_out` (clean level-2 pass) gives score 2 and sets `unlocked_at` of the subtopic itself
  (one-way); a review card is created from that day (SPEC 5.4).
- `GET /subtopics/{id}` `checks[]` now lists the items of `content/checks` by level (it used to
  read the lesson's `mastery_check` lists, empty in hand-written lessons).
- Since T2.2b the loader derives `has_l2_items` / `has_l3_write_code` from `content/checks`, which
  removes the M1 shortcut (a clean practice AC alone = score 2) for every subtopic with checks.

## Review (Leitner, SPEC 5.4)

### `GET /api/review/queue[?editor=false]`

All due cards (`due_on <= today` in the user's tz, not suspended), most overdue first, tie-break
lowest score. No cap. Returns `{today, total_due, backlog_warn, backlog, cards[], short_session}`.
Card: `{subtopic_id, name_vi, box, due_on, overdue_days, score, lapses, item_kind, item, recall_item}`.
`item` = `{kind, ref, type, subtopic_id}`: boxes 1-2 a recall item (a graded lesson block
`<sid>#<block>`, else a level-1 non-write_code check `check:<sid>:<item_id>`; rotated by the number
of past reviews); boxes 3-5 a code problem (level-2/3 check problem, then practice problem; not yet
clean first, then least recently attempted), falling back to recall when none exists or with
`editor=false`. `recall_item` is the recall fallback for boxes 3-5. `short_session` is a hint only:
`{enabled, size (settings.review_preset, null = off), max_code: 2, cards: [{subtopic_id, item_kind}]}`
where code cards beyond the second are demoted to recall.

### `POST /api/review/{subtopic_id}/result`

Body `{success, item_ref?, item_kind?}`. With `item_ref` the kind is derived (a known problem id =
`code`, anything else `recall`; a conflicting `item_kind` is `422 item_kind_mismatch`). With only
`item_kind` the server picks that kind's item. Applies `leitner.review` from the real review day,
appends `review_log` (`item_ref, item_kind, box_before, box_after, success`), updates the card,
records a `review_result` event and recomputes the score (`retention_ok` reads `review_log`).
Returns `{subtopic_id, success, item_ref, item_kind, box_before, box_after, due_on, lapses,
score: {before, after}, newly_unlocked}`. Errors: `404 review_card_not_found`, `409 card_not_due`,
`422 missing_field | item_kind_mismatch | no_review_item`. Honors `Idempotency-Key`.

## Navigation and activity (T2.5, SPEC 5.5)

### `GET /api/next`

Returns `{must_raise[], up_next[], locked_preview[], due_count, backlog, study: {today_s, week_s}}`.
No current-day, quota, "late" or schedule field (self-paced, SPEC 5.5).
- `must_raise`: up to 5 entries, one per prerequisite with score exactly 1 that blocks a locked
  subtopic — `{prerequisite: {id, name_vi, score, need: 2}, unlocks: {id, name_vi}, sole_blocker,
  also_blocks, suggested_problem, test_out: {available, retry_after}}`.
- `up_next`: unlocked, not-`done` subtopics (`done` = score ≥ max(1, target_intern)), ordered
  in-progress first, then plan order `(N, position)`, then check-retry-locked last. Each:
  `{id, name_vi, status, score, check_retry_after, due_card, known_basic, suggested_problem, ...}`.
- `locked_preview`: 3 locked items with lock reasons. `due_count`/`backlog` from the review queue.

### `POST /api/activity/ping`

Adds `min(now - last_ping, 60s)` to the user's `study_time` for today, ignoring gaps > 120s (which
still move `last_ping` forward; it never goes backward), so a resend or a second tab adds ~0.
Optional `{resume}` body updates `resume_state` like `PUT /resume`. Returns `{added_s, today_s,
week_s}`. `last_ping` lives in a new `activity_state` table (addition beyond SPEC 6.3); `study_time`
is `(user_id, day) -> seconds` (SPEC 6.3). Migration `0003_study_time`.

## Placement, Phase A (A10)

Engine `services/placement.py`, router `routers/placement.py`, table `placement_sessions`
(migration `0005_placement`). Evidence is only `check_results` (`context=placement`) written through
`checks.answer`; the score is recomputed by `scoring.py`, so placement seeds score 2 (clean level-2
`write_code` = `tested_out`) and never 1 or 3. Level 3 is never asked. A level-1 pass sets
`known_basic` only. Graph inference is `user_subtopic.placement_hint` (`likely_known`/`likely_gap`),
a label cleared by real evidence.

- `POST /api/placement` `{experience?, restart?, skip?}`: start, or resume the sitting in progress
  (`resumed: true`). `skip` = "Bắt đầu từ đầu": a `skipped` session, writes no results (also sets the
  A8 `placement_choice`). `GET /api/placement/current` (latest sitting or `{placement: null}`),
  `GET /api/placement/{id}`.
- `POST /api/placement/{id}/answer` `{item_id, elapsed_ms, session_elapsed_ms?, gave_up?, code,
  verdict, passed_tests, total | answer | self_grade}` (same fields as a check answer);
  `POST .../skip` `{item_id}` = "Không biết" (give-up: no lock, not a pass);
  `POST .../heartbeat` `{active_ms, item_elapsed_ms?}` (absolute, monotonic, capped by the wall
  clock); `POST .../finish` (keeps what was measured); `GET .../result` (seeded skill map,
  strong/weak areas, `start`, `content_pending`, `test_out_candidates`).
- View: `{placement_id, status, stop_reason, message_vi, active_ms, budget{soft,hard,remaining},
  progress{gates_total,gates_done}, gates[{code,subtopic_id,outcome,l1,retry_after}], current{gate,
  subtopic_id, check_session_id, elapsed_ms, step{index,count,item...}}}`.
- Rules: entry gate by `experience` (none C1, some C2, solid C3; `none` runs C1 -> C2 only); pass
  goes up; a failed/given-up gate stops once the gate below was tried (that one is asked if not yet
  measured); no gate below: stop at once. No new gate when `active_ms + minutes > 60 min`.
- `GET /me.onboarding.placement` is `none | in_progress | finished | skipped`.

## Not in this document yet

Placement Phase B/C (A11b, M2b), `kind=continue|retake`.
