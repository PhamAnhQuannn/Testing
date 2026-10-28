# Review: sd.archetypes.workflow_engine

**Verdict: PASS (clean, publishable as-is).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Durable execution model is correct and current: durable event history as source of truth; replay re-drives from history, returning recorded results for completed steps and only executing steps not yet in history, reconstructing in-memory state and continuing from the crash point. Matches Temporal/Cadence/Step Functions (2026).
- Three core components (durable event history, task queue, timer service) correctly described; timer-as-a-row explanation for millions of waiting workflows is accurate.
- Both mandatory constraints are right: (1) activities must be idempotent because at-least-once delivery + replay can re-drive a step (crash after side effect, before recording) → idempotency key → effectively-once; (2) workflow code must be deterministic — no direct wall-clock/random, use engine-provided APIs whose values are written to history so replay reproduces the same path.

## Special checks (all pass)
- Durable event history + replay recovery: present and correct (b02, b03, b11).
- Idempotent activities + deterministic workflow code: both covered with correct rationale (b07–b09, S242, S243).

## Quiz / check items
- b04, b06, b09 (MCQ) and b08 (fill): all answers and explanations correct; distractors are genuinely wrong and explained.
- S241 (diff1 recall): correct, matches level-1 recall.
- S242 (diff2 score-2 scenario): the "crash after charge succeeds but before recording" scenario correctly yields re-drive → requires idempotency; rubric sensible.
- S243 (diff3 interview): matches mastery_bar_vi (draw engine with durable history/task queue/timer, explain replay recovery, explain why steps must be idempotent). Rubric level-appropriate.

## Reuse of taught concepts
- Correctly reuses saga/event-driven (sd.async.event_driven_patterns), task workers (sd.async.task_workers), delivery guarantees/at-least-once/effectively-once (sd.async.delivery_guarantees), scheduler (sd.archetypes.job_scheduler). Applies rather than re-teaches.

## Language
- Vietnamese clear; English terms consistently parenthesized (durable execution, durable event history, task queue, timer service, idempotent, deterministic, at-least-once, effectively-once).

No must-fix items.
