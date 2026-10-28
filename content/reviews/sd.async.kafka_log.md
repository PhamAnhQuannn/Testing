# Review: sd.async.kafka_log

**Verdict: PASS (clean).** Independent content review, 2026-10-27.

## Technical accuracy & currency (2026)
- Distributed commit log framing correct: append-only, partitioned, replicated; retention + per-consumer offset → replayable and independent consumer groups, contrasted with classic queue (delete-on-ack). Accurate.
- Partition routing correct: `hash(key) % num_partitions` (lesson says "đại ý", appropriately hedged); same key → same partition → per-key order. Default Kafka uses murmur2/sticky for null keys, but the conceptual statement is correct for interview level.
- Consumer group semantics correct: each partition assigned to exactly one consumer in a group; one consumer may hold several partitions; extra consumers idle (standby for rebalancing).
- Partition sizing guidance sound: target throughput / per-consumer throughput + margin; too-few vs too-many trade-off; increase easy / decrease unsafe; increasing partitions changes key hashing and can break existing per-key order. Correct and current.

## SPECIAL checks
- Ordering ONLY within a partition: stated explicitly and repeatedly. Correct.
- Partition key routing: correct.
- Consumer group = one consumer per partition, parallelism bounded to #partitions: correct ("số consumer hữu ích tối đa = số partition").
- Consumer lag = offset behind log end: `(offset cuối log) − (offset đã đọc)`. Correct.

## Quizzes
- b04 (order per account on 4-partition topic): answer `a` correct; (b) no cross-partition reordering, (c) 1-partition not the *only* way — both rebuttals accurate.
- b06 (3 partitions, 5 consumers): answer `b` correct; (a) partition not split, (c) extra consumers legal not error — accurate.
- b09 (lag rising, 4 consumers on 4 partitions, CPU-bound): answer `b` correct; (a) over-cap, (c) retention cut only deletes old data — accurate.

## Mastery items vs bar
Bar: "giải thích Kafka giữ thứ tự bằng partition key, chọn số partition và xử lý consumer lag."
- S112 (diff1 recall): order scope + partition key. Correct.
- S113 (diff2 score-2 scenario): 3000/500 → ≥6 partitions, key=order_id, 4<6 consumers bound by consumer count. Correct arithmetic and reasoning; rubric sensible.
- S114 (diff3 interview): ordering + partition sizing (both too-few/too-many) + lag reduction order. Matches bar; rubric gates the "consumer ≤ partition" ceiling.
- Items only test taught ideas (b03–b08). 

## Language
Vietnamese clear; English terms parenthesized (commit log, partition, offset, retention, consumer group, rebalancing, consumer lag).

No must-fix issues.
