# Review: sd.async.event_driven_patterns

**Verdict: PASS (clean).** Independent content review, 2026-10-27.

## Technical accuracy & currency (2026)
- Four patterns each framed as problem + cost, which matches the bar.
- Event sourcing correct: immutable append-only event log is source of truth; state rebuilt by replay; benefits = audit + time-travel; costs = replay cost (needs snapshots) + hard schema evolution (events stored forever; add optional fields only) + corrections need compensating events. Accurate (schema-evolution simplification is interview-appropriate).
- CQRS correct: separate write model from read model(s)/projection; command → write → event → projection builds read-optimized table; reads scale independently; cost = eventual consistency + more moving parts. Accurate.
- Saga correct: long distributed transaction as chain of local transactions + compensating actions instead of 2PC; orchestration vs choreography described accurately; cost = hard to reason about mid-failure, compensations must be idempotent, intermediate visible state. Correct.
- Outbox correct: same-DB-transaction outbox row + relay/CDC (Debezium) publish; cost = extra table/process, delay, at-least-once so receiver must be idempotent. Accurate and current.

## SPECIAL checks
- Each pattern: problem + cost + when-not-to-use: all present (b02–b05, b07, b09).
- Saga uses compensating actions, NOT 2PC: correct, and explicitly contrasts 2PC.
- order→payment flow sound: create → reserve inventory → charge → ship; on charge failure → release inventory + cancel; on ship failure → refund + release. Correct and consistent.

## Quizzes
- b04 (event sourcing source of truth + cost): answer `b` correct; (a) plain state-store, (c) CQRS read model — accurate rebuttals.
- b06 (saga, ship fails): answer `b` (compensate: refund then release) correct; (a) 2PC is what saga avoids, (c) infinite retry abandons money/stock — accurate.
- b08 fill (outbox): correct, accept list reasonable.

## Mastery items vs bar
Bar: "với mỗi mẫu trong bốn mẫu, nêu vấn đề nó giải, vẽ luồng cho ví dụ đặt hàng thanh toán và nêu khi nào không nên dùng."
- S121 (diff1 recall): name four + one-line problem each. Correct.
- S122 (diff2 score-2 scenario): read-heavy product page → CQRS flow + cost + CRUD "don't use". Correct; rubric sensible.
- S123 (diff3 interview): all four patterns × (problem, order→payment flow, when-not). Matches bar exactly; rubric requires all four + saga compensation + outbox same-txn.
- All items test taught ideas. 

## Language
Vietnamese clear; English terms parenthesized (event sourcing, CQRS, saga, outbox, source of truth, replay, snapshot, schema evolution, eventual consistency, compensating action, orchestration, choreography, CDC).

No must-fix issues.
