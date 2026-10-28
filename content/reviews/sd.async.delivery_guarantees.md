# Review: sd.async.delivery_guarantees

**Verdict: PASS (clean).** Independent content review, 2026-10-27.

## Technical accuracy & currency (2026)
- Three semantics correct: at-most-once (can lose, never duplicate), at-least-once (never lose, can duplicate), exactly-once (ideal, hardest). "Over an unreliable link you really only choose lose-vs-duplicate" is the right framing.
- ack-vs-process timing correct: at-most-once = ack before process (lose on crash after ack); at-least-once = process before ack (duplicate if crash before ack). at-least-once as practical default: correct.
- "exactly-once = at-least-once + idempotency/dedup at receiver" correctly stated, with message-id/idempotency-key + dedup store → exactly-once *effect*. Accurate and well-phrased.
- Dual-write problem correctly explained (DB-commit-then-publish can drop; publish-then-DB can ghost; two systems can't share one transaction).
- Transactional outbox as 2 steps correct: step 1 = single DB txn writing business row + outbox row (commit/rollback together); step 2 = relay/CDC reads outbox, publishes, marks sent; step 2 is at-least-once so receiver still dedups. Correct.

## SPECIAL checks
- at-most/at-least/exactly-once: correct.
- "exactly-once = at-least-once + idempotency/dedup": correct.
- 2-step transactional outbox (same-txn business+outbox, then relay publishes): correct and precise.

## Quizzes
- b03 (process-then-ack, redeliver on crash): answer `b` (at-least-once) correct; (a)/(c) rebuttals accurate.
- b05 (practical exactly-once for payments): answer `b` correct; (a) at-most-once can lose payment, (c) can't trust broker — accurate.
- b07 (what outbox does in step 1): answer `b` (business + outbox in one txn) correct; (a) ghost, (c) still dual-write — accurate.

## Mastery items vs bar
Bar: "thiết kế pipeline chịu tin trùng, giải thích exactly-once thực chất là at-least-once cộng idempotency và vẽ outbox 2 bước."
- S115 (diff1 recall): three semantics + practical default. Correct.
- S116 (diff2 score-2 scenario): at-least-once double-charge → idempotent consumer + dedup store → exactly-once effect. Correct; rubric sensible.
- S117 (diff3 interview): exactly-once reasoning + dedup placement + dual-write + 2-step outbox + still-need-dedup + reconciliation. Matches bar; rubric gates both outbox steps.
- Reconciliation (safety net) is taught in b08 callout, so S117 does not test untaught material. 

## Language
Vietnamese clear; English terms parenthesized (delivery semantics, idempotency, dedup, dual-write, transactional outbox, CDC, reconciliation).

No must-fix issues.
