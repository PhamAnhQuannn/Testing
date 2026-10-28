# Review: sd.async.queues_pubsub

**Verdict: PASS (clean).** Independent content review, 2026-10-27.

## Technical accuracy & currency (2026)
- Async messaging rationale correct: decouple, absorb spikes (buffer), smooth load; consumer pulls at its own rate. Accurate.
- Queue vs pub/sub distinction is the right one: queue = point-to-point, one message to exactly one consumer in the group (competing consumers); pub/sub = fan-out, one message to every subscriber. Selection heuristic ("one place does it → queue; many need to know → pub/sub") is sound.
- ack + visibility timeout correct: broker hides (not deletes) on pull, deletes only on ack, reappears on timeout without ack. Trade-off (too short → duplicate work while old worker still running; too long → stuck message on crash) is accurate.
- retry + backoff + jitter correct; DLQ after max attempts for poison messages, keeps main flow unblocked. Accurate.
- at-least-once default → consumer should be idempotent; correctly deferred deep-dive to later lesson.

## SPECIAL checks
- queue (one consumer) vs pub/sub (fan-out): correct.
- ack, visibility timeout, retry, DLQ: all correct and precisely described.

## Quizzes
- b03 (fan-out to 3 systems → pub/sub): answer `b` correct; (c) competing-consumers rebuttal accurate.
- b06 (worker dies before ack): answer `b` correct; (a)/(c) rebuttals accurate (not deleted on pull; DLQ only after max attempts).
- b07 fill (DLQ): correct, regex + accept list robust.

## Mastery items vs bar
Bar: "chọn queue hay pub/sub cho từng tình huống và mô tả ack, visibility timeout, retry và DLQ."
- S109 (diff1 recall): core difference + one example each. Correct, recall level.
- S110 (diff2 score-2 scenario): queue between API and email workers; 2 benefits, ack/visibility-timeout no-loss, DLQ for poison. Correct, right difficulty; rubric sensible.
- S111 (diff3 interview): choose queue for (A) + pub/sub for (B), full reliable-delivery flow, at-least-once → idempotent. Matches bar exactly; rubric gates all 4 mechanisms.
- Items only test taught ideas (b01–b08). 

## Language
Vietnamese clear; English terms consistently parenthesized (decouple, competing consumers, fan-out, visibility timeout, poison message, DLQ, idempotent).

No must-fix issues.
