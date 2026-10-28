# Review: sd.archetypes.ad_click_aggregation

**Verdict: PASS (clean, publishable).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Two-path (lambda) architecture correct: streaming path = fast/approximate for dashboard (minute windows, event time + watermark, upsert to OLAP), batch path = end-of-day reprocess of raw log from object store, full dedup → authoritative number for billing. Reconciliation/alert on drift included.
- Streaming approximations correctly stated: late events dropped after watermark; at-least-once can double-count on job restart.
- "302 redirect after logging click to Kafka" pattern correct and current.
- Top-K: Count-Min Sketch (over-estimates only) + size-K min-heap for heavy hitters; sliding 1h window via 60 per-minute tables summed. Correct.

## Special checks (all pass)
- Two-path stream-approximate / batch-authoritative for billing: present and correct (b03, b06, S247, S249).
- Hot-key salting: ad_id#0..9 spread across partitions, count separately, sum at query time; correctly explains that merely adding partitions does NOT help (same key still maps to one partition). (b08, b09, S248)
- Click dedup: impression id HMAC-signed, verify signature, seen-set via Redis SET NX + TTL; batch also dedups by same impression id. (b10, b11)
- Why batch number is billed: correct — billing needs exactness; batch reprocesses settled raw log with thorough dedup → source of truth. (b07, S249)

## Quiz / check items
- b05, b07, b09 (MCQ), b11 (fill): answers and explanations correct; distractors genuinely wrong (sampling for billing, double partitions, etc.).
- S247 (diff1), S248 (diff2 hot-key scenario), S249 (diff3 interview matching mastery_bar_vi: two-path pipeline + hot-key salting + dedup + why end-of-day billing): correct, level-appropriate, rubrics sensible.

## Reuse of taught concepts
- Reuses data pipeline / Kafka buffer (sd.archetypes.data_pipeline), windowing/event-time/watermark (sd.async.stream_processing), Count-Min Sketch + heap (sd.data.probabilistic_structures). Applies, not re-teaches.

## Language
- Vietnamese clear; English terms parenthesized throughout.

## Minor (non-blocking, not must-fix)
- Block ids skip b04 (sequence runs b01, b02, b03, b05, ...). Cosmetic; does not affect content or rendering. Flag to author in case the schema/validator expects contiguous ids.

No must-fix items.
