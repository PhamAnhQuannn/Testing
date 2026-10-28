# Review: sd.archetypes.job_scheduler

**Verdict: APPROVE** (no must-fix). Reviewer: independent content pass, 2026-10-27.

## Technical accuracy & currency
- Job types (run-now, one-off, recurring/cron) and per-job run_at + state storage correct. cron "0 8 * * *" = 8am daily correct.
- Store + find-due: indexed run_at query, time-bucketed index, timing wheel, delay queue — all valid options, correctly motivated (avoid full-table scan). Recurring recompute of next run_at from cron after execution — correct.
- Scheduler tier (scan due -> enqueue) + worker pool, independent scaling — correct, matches special-check.
- Duplicate-execution avoidance: leader election / distributed lock OR atomic claim via conditional UPDATE (`SET state='running' WHERE id=X AND state='waiting'`) — correct; notes atomic claim spreads scan load better than a single leader. Good nuance.
- at-least-once -> idempotent jobs: correctly grounded in heartbeat/lease reassignment of orphaned jobs as the source of re-execution; dedupe by unique run id before side effects. Retry+backoff -> DLQ correct.
- Missed-execution catch-up policy (run-all / latest-only / skip), backpressure, priority/fairness, state machine (waiting->running->done/failed) all present.

## Checks
- b04 (a), b06 (a), b08 fill (idempotent / run id / DLQ) — answers + explanations correct; fill accepts VN + EN synonyms.
- S196 diff1 recall (job types + indexed run_at): correct, rubric sensible (requires one-off + recurring and the index point).
- S197 diff2 score-2 (multi-scheduler dup risk + atomic claim mechanics): correct; explanation of why only one UPDATE wins is accurate.
- S198 diff3 interview: full design matching mastery_bar (run_at index, conditional claim, heartbeat, why idempotent). Rubric aligns.

## Pedagogy / language
- Reuses sd.async.task_workers and sd.distributed.distributed_locks by reference, not re-teaching.
- Vietnamese clear; English terms parenthesized.

No corrections required.
