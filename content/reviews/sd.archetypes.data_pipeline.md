# Review: sd.archetypes.data_pipeline

**Verdict: APPROVE** (no must-fix). Reviewer: independent content pass, 2026-10-27.

## Technical accuracy & currency
- Three-tier frame (ingestion -> processing -> sinks) with Kafka as durable buffer / decoupler (backpressure absorption, retention for replay) — correct and current.
- Ingestion: SDK/collector or CDC into partitioned Kafka; partition-key choice, skew, hot-key salting — correct.
- **lambda vs kappa verified**: lambda = two branches (stream + batch, two codebases); kappa = single stream branch, recompute by replay of the event log. Correct.
- Two sinks: stream -> OLAP (columnar, sub-second dashboards) + data lake (Parquet/S3 by day) as source of truth for replay — correct.
- **exactly-once / idempotent verified**: at-least-once -> possible duplicates (esp. on replay) -> idempotent sink via event_id dedup or key upsert (e.g. (product, hour)) — correct. Schema registry + compatibility (additive OK, type change blocked) + DLQ for bad-schema events — correct. Backfill correct.
- **Estimation verified exactly**: 100,000 ev/s x 1 KB = 100 MB/s = 8.64 TB/day; /5 columnar = 1.73 TB/day; Kafka 7d x 3 replicas = 8.64 x 21 = 181.44 TB (~180 TB). All numbers in lesson (b07) and S180 match.

## Checks
- Quiz b03 (a, Kafka durable buffer/decouple), b05 (a, lambda two-branch vs kappa replay), b09 fill (idempotent) — all answers + explanations correct.
  - Minor note (not a fix): b09 fill also accepts "upsert"; the prompt asks specifically for the one-word term meaning "same result when rerun" (= idempotent). Upsert is a technique, not the term, but accepting it is lenient and the explain_md covers both. Fine to leave.
- S178 diff1 recall (3 tiers + Kafka role): correct; rubric sensible.
- S179 diff2 score-2 scenario (product views/hour): answer correct (partition by product_id, two sinks, idempotent); rubric sensible.
- S180 diff3 interview: matches mastery_bar level 3 (pipeline source->reporting with two sinks, capacity estimate, schema management, recompute on error). Rubric aligns. Good.

## Pedagogy / language
- Reuses prerequisites (kafka_log, stream_processing, delivery_guarantees) by naming where each was taught and applying — explicitly does not re-teach.
- Vietnamese clear; English terms parenthesized consistently.

No corrections required.
