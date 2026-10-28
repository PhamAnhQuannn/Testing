# Review: sd.api.async_apis

**Verdict: PASS (clean).** Independent content review, 2026-10-27.

## Technical accuracy & currency (2026)
- Sync-vs-async framing correct: long work on an open connection → proxy/LB timeout (30–60s), client blocked, duplicate execution on retry. Accurate.
- async request-reply correct: `POST` returns **202 Accepted** + job id + status URL (`Location` header or body), work runs in background; client learns result via polling (`GET /jobs/{id}`, `Retry-After`) or callback/webhook. Accurate; state machine `queued → running → done/failed`.

## SPECIAL checks
- 202 + status/polling vs callback: correct (b02, b03, S106).
- Reliable webhook: all five properties correct (b04, b05) — sender: HMAC signing with shared secret + retry with exponential backoff + DLQ; receiver: verify signature + replay protection (timestamp/nonce) + idempotent by event id. Correctly ties "at-least-once delivery" to the mandatory idempotent receiver.
- SSE token streaming: correct (b07) — one-way server→client `text/event-stream`, push tokens as generated, lighter than bidirectional WebSocket, reduces time-to-first-token, supports mid-stream cancel by closing the connection. S108 correctly notes the stream can open via `GET` or `POST`, matching real LLM APIs.

## Quizzes
- b03 (2-min export → return immediately): answer `b` (202 + job id + status URL) correct; `a`/`c` rebuttals accurate.
- b06 (why receiver must be idempotent): answer `a` correct; `b` (HMAC is source/integrity, not delivery count) and `c` correctly dismissed.
- b08 fill (`202`, `SSE`): both correct; accept lists reasonable.

## Mastery items vs bar
Bar: "thiết kế API cho job dài và webhook đáng tin cậy, và API stream token cho ứng dụng LLM."
- S106 (diff1 recall): what async request-reply does + 202 + two result channels. Correct, recall level.
- S107 (diff2 score-2 scenario): partner 5xx / double-charge webhook — sender retry+DLQ, HMAC verify, at-least-once → idempotent receiver. Correct; rubric gates on idempotent/at-least-once + signature verify.
- S108 (diff3 interview): design all three APIs (long job + idempotency-key against duplicate jobs, reliable webhook both sides, SSE token stream with rationale) — matches the bar exactly. `answer_md` correct; rubric gates on failure handling (retry/DLQ/idempotent).
- Items only test lesson-taught ideas.

## Language
Vietnamese clear; English terms parenthesized (202 Accepted, Retry-After, HMAC, shared secret, replay, dead-letter queue, at-least-once, SSE, Server-Sent Events, WebSocket). 

No must-fix issues.
