# Review: sd.api.idempotency

**Verdict: PASS (clean).** Independent content review, 2026-10-27.

## Technical accuracy & currency (2026)
- Definition correct: one-or-many executions → same effect; safe to resend. Elevator analogy good; "trừ 100k hai lần = 200k" correctly illustrates non-idempotent.
- HTTP classification correct (RFC 9110): GET/PUT/DELETE idempotent, POST not by default. DELETE-twice framing (state still "gone") is right.
- Idempotency-key pattern correct: client generates a unique key per *intent*, sends in `Idempotency-Key` header; server stores key → (state, stored response); replay returns stored response without re-executing. Matches Stripe/IETF practice.

## SPECIAL checks
- GET/PUT/DELETE idempotent vs POST not: correct (b02, b03, S103).
- Idempotency-key pattern: correct and complete (b04, b05).
- Unknown-result-timeout handling: correct (b06, b07) — retry with the *same* key; landed → return stored result, not-landed → execute exactly once; store key+response, set TTL (24h example).
- Concurrent-duplicate race (b08, b10): correctly requires atomic register-then-act via unique constraint (one INSERT wins) or per-key lock; identifies the check-then-write gap precisely.

## Quizzes
- b03 (which is non-idempotent → POST /charges): answer `c` correct; explain accurate.
- b05 fill (`idempotency key`): correct; accept list covers EN/VN variants.
- b07 (timeout, unknown result): answer `b` correct; `a` (new key = new transaction) and `c` (skip retry) rebuttals accurate.
- b10 (why atomic check-and-set): answer `b` correct; `a`/`c` correctly dismissed.

## Mastery items vs bar
Bar: "thiết kế idempotency key cho endpoint thanh toán và xử lý đúng trường hợp timeout không rõ kết quả."
- S103 (diff1 recall): define + classify methods. Correct, recall level; rubric sound.
- S104 (diff2 score-2 scenario): POST /charges timeout — client action + server mechanism + what to store. Correct; rubric gates on same-key retry + stored response.
- S105 (diff3 interview): design the key + handle (a) first call, (b) timeout-unknown-result, (c) concurrent duplicates — matches bar and extends it correctly. Reconciliation mention is taught in b09. `answer_md` correct; rubric gates on the two hard cases (b) and (c).
- Items only test lesson-taught ideas.

## Language
Vietnamese clear; English terms parenthesized (idempotency, unique constraint, lock, TTL, reconciliation). 

No must-fix issues.
