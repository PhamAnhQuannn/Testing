# Review: sd.async.task_workers

**Verdict: PASS (clean).** Independent content review, 2026-10-27.

## Technical accuracy & currency (2026)
- Background job rationale correct: offload slow work (email, thumbnail, export, transcode) to queue + worker pool; request returns immediately. Celery/Sidekiq named accurately.
- Retry correct: exponential backoff (1s,2s,4s,8s...) + jitter to avoid synchronized retry storm / thundering herd; max attempts then DLQ for poison job. Accurate.
- Idempotency correctly motivated: at-least-once (worker dies after work before ack, or visibility timeout) → job may run twice → idempotency key (order_id/job_id) + record-done + skip-if-seen / conditional write. "at-least-once forces idempotent" is correctly the central idea. "Exactly-once end-to-end nearly impossible" is accurate.
- Rate control correct: concurrency cap (avoid exhausting connection pool / downstream), downstream rate limiting (token bucket), per-tenant fairness (dedicated/priority queues, round-robin), priority queues so urgent work isn't stuck behind slow. Accurate.
- Status tracking correct: pending → running → succeeded/failed state machine, progress, result storage, attempt count/last error; polling or notify; feeds autoscaling by queue depth. Accurate.

## SPECIAL checks
- retry + backoff + jitter + DLQ: correct.
- idempotency needed because at-least-once: correct and emphasized.
- rate control: correct (concurrency, downstream rate-limit, per-tenant fairness).
- status tracking: correct.

## Quizzes
- b03 (why backoff + jitter): answer `b` correct; (a) jitter adds wait, (c) DLQ unrelated — accurate.
- b05 (avoid two emails under at-least-once): answer `b` (idempotent + "sent" flag) correct; (a) disabling retry loses reliability, (c) big visibility timeout doesn't stop crashes — accurate.
- b07 fill (DLQ / idempotent): both correct, accept lists reasonable.

## Mastery items vs bar
Bar: "thiết kế hệ worker an toàn với retry và việc chạy trùng, điều tốc độ và theo dõi trạng thái job."
- S124 (diff1 recall): job system purpose + retry/backoff + DLQ after max attempts. Correct.
- S125 (diff2 score-2 scenario): double-charge → at-least-once cause + idempotency fix + why not exactly-once. Correct; rubric sensible.
- S126 (diff3 interview): full thumbnail worker (queue+pool, retry/DLQ/poison, idempotency, rate/fairness, status, worker-dies). Matches bar exactly.
- All items test taught ideas. 

## Language
Vietnamese clear; English terms parenthesized (background job, worker pool, exponential backoff, jitter, thundering herd, max attempts, DLQ, visibility timeout, idempotent, per-tenant fairness, token bucket, autoscaling).

No must-fix issues.
