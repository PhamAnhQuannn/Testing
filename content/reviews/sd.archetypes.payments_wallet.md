# Review: sd.archetypes.payments_wallet

**Verdict: APPROVE** (no must-fix). Reviewer: independent content pass, 2026-10-27.

## Technical accuracy & currency
- Correctness-over-scale framing + strong consistency for balances + exactly-once effect — correct.
- Double-entry ledger: append-only, balanced debit/credit pairs, balance = sum of lines, global invariant (sum of all lines = 0), immutable audit trail — all correct and the special-check's core.
- Idempotency keys for exactly-once effect (store result by key, replay returns stored result, never re-debit) — correct; correctly tied to sd.api.idempotency.
- Double-spend prevention: conditional/atomic debit in a single transaction OR row lock; "check sufficient funds" and "write debit line" must be inseparable — correct.
- Cross-service transfer: single ACID transaction / 2PC when one DB; saga + compensating action across services. Correctly requires every step AND every compensation to be idempotent, and at-least-once + dedup for messaging — matches special-check.
- PSP (Stripe) + webhook: idempotency key on call, webhook may be duplicate/out-of-order -> idempotent receiver + signature verification + forward-only state lifecycle (authorize->capture->settle->refund) — correct.
- Unknown-result timeout: query status before retry OR retry with same idempotency key, never a new one — correct (this is the key distinction).
- Reconciliation job + audit trail to catch drift — present.

## Checks
- b03 (b), b06 (c), b08 (b) — answers + explanations correct. b06 correctly frames timeout as unknown outcome, not failure.
- S199 diff1 recall (ledger pair + why append-only): correct, rubric sensible.
- S200 diff2 score-2 (3x resend + concurrent withdraw + PSP timeout): correct across all three sub-parts, rubric sensible.
- S201 diff3 interview (P2P across two services + PSP): full design matching mastery_bar (no double-charge, ledger + state lifecycle, timeout + reconciliation). Rubric aligns and explicitly requires idempotent compensation + correct timeout handling.

## Pedagogy / language
- Reuses sd.api.idempotency, sd.distributed.distributed_transactions, sd.async.delivery_guarantees by reference.
- Vietnamese clear; English terms parenthesized. Forward-link to trading_brokerage is appropriate.

No corrections required.
