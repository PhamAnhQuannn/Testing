# Review: sd.archetypes.notification_system

**Verdict: APPROVE** (no must-fix). Reviewer: independent content pass, 2026-10-27.

## Technical accuracy & currency
- Multi-channel pipeline (producer -> notification service -> per-channel queue + worker -> provider) is correct and current for 2026. APNs/FCM naming correct.
- Per-channel queue/worker + priority queue (OTP vs campaign) rationale is sound and matches the special-check requirement.
- Retry (exponential backoff + jitter, transient-only: timeout/5xx/429), provider failover + circuit breaker, DLQ: all accurate. Correctly distinguishes transient vs permanent errors (bad number, unregistered token).
- at-least-once -> idempotency/dedup framing is correct: worker crash after provider call before ack. Dedup key (user_id, type, event_id) in Redis+TTL is a standard, correct pattern.
- User prefs/opt-out/quiet hours/per-user rate limit covered. Batching/digest + fan-out by batch for broadcast correct.
- Webhook: HMAC-signed payload + timestamp (anti-replay), retries+backoff+DLQ, receiver idempotency via event_id, per-customer isolation, delivery-status tracking — all present and correct.

## Checks
- Quiz b03 (a), b06 (b), b09 fill "idempotent" — all answers + explanations correct.
- S187 diff1 recall: correct, rubric sensible (both halves required).
- S188 diff2 score-2 scenario (dup + lost on timeout): answer correct, rubric sensible.
- S189 diff3 interview: matches mastery_bar level 3 (burst-tolerant, dedup, prefs, provider failover). Rubric aligns to the bar. Good.

## Pedagogy / language
- Correctly reuses prerequisites (task_workers, queues_pubsub) without re-teaching.
- Vietnamese clear; English terms parenthesized consistently.

No corrections required.
