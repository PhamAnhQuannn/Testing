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

## Not in this document yet

Placement, review, `/next`, `/activity/ping` (later A-tasks).
