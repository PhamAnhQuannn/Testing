# Review: sd.distributed.distributed_transactions (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

9 blocks; graded: b03 (mcq), b05 (mcq), b08 (fill). mastery_check l1 [S139], l2 [S140], l3 [S141].
mastery_bar_vi: "chọn 2PC hay saga và thiết kế bước bù idempotent cho luồng thanh toán hoặc đặt chỗ." — S141 covers all.

## Technical accuracy (verified)
- 2PC: coordinator runs prepare (participants do work, hold locks, vote ready/no) then commit (all ready → commit, any no → abort). Gives true atomicity but (1) **blocking** (locks held across both phases → throughput drop) and (2) coordinator is **single point of failure** — dies after prepare → participants stuck holding locks, cannot decide. Rarely used across microservices; better for few close DBs needing strict atomicity. Correct.
- Saga: sequence of local transactions, each commits in its own system; cannot rollback a committed step, so each has a **compensating action** to undo when a later step fails (debit → reserve seat; reserve fails → compensate refund). Choreography (event-driven, no central coordinator, loose coupling, hard to observe) vs orchestration (central orchestrator, observable, must be maintained). Correct.
- Saga trade-off correctly stated: higher availability (no cross-locks) but only **eventual consistency** and **no isolation** — intermediate dirty state visible (money debited, no seat yet). Compensating steps must be **idempotent** because retries may re-invoke them (double refund is wrong). Correct. Saga is clearly NOT framed as 2PC.
- TCC (Try-Confirm-Cancel): a saga with explicit reservation — Try reserves/holds, Confirm finalizes, Cancel releases; Confirm/Cancel also idempotent. Correct.
- Selection guidance (few close DBs + instant atomic → 2PC; many services + long tx → saga/TCC + periodic reconciliation) sound.

## Quiz / mastery correctness
- b03 [b] participants stuck holding locks after coordinator dies post-prepare: correct; (a) no auto-abort (no command arrives), (c) 2PC does not let participants self-decide — refuted correctly.
- b05 [b] higher availability, eventual consistency, no isolation, dirty state visible: correct; (a) saga does not cross-lock, (c) needs compensation (not instantly atomic) — refuted correctly.
- b08 fill: "compensating" + "idempotent": correct; accept lists cover variants.
- S139 (L1): two phases + two weaknesses. Sensible.
- S140 (L2 scenario): ticket booking saga — compensation on failed step, eventual/no-isolation trade-off, why idempotent. Correct, good score-2 item.
- S141 (L3 interview): payment flow — choose saga/TCC with justification, design compensating steps + idempotency (idempotency key / state check), a real risk + mitigation (TCC, reconciliation, bounded retry). Matches mastery_bar; correct.

## Coverage discipline
Mastery items test only taught ideas. No leakage.

## Language
Vietnamese clear; English terms parenthesised (distributed transaction, 2PC/two-phase commit, coordinator, prepare/commit/abort, blocking, single point of failure, saga, local transactions, compensating action, choreography/orchestration, eventual consistency, isolation, idempotent, idempotency key, TCC/try-confirm-cancel, reservation, reconciliation). Good.

## Findings
None blocking. Accurate and interview-correct.
