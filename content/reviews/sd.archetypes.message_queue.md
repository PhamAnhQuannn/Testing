# Review: sd.archetypes.message_queue

**Verdict: APPROVE (clean).** Independent content review, 2026.

- Technical accuracy: broker built up correctly — append-only log (sequential write fast, segmented ~1 GB, sparse index, delete by dropping whole segment) → partitions (per-partition log, horizontal scale, ordering only within partition, key-based partitioning, consumer-group parallelism capped by partitions) → replication (leader handles reads+writes, followers copy, failover to an in-sync follower). All correct and current.
- Special check (acks + ISR): ISR = replicas keeping up; a record is committed only when written to all replicas in the ISR; acks=0 (fire-and-forget) / acks=1 (leader only, loses data if leader dies before follower copies) / acks=all (waits for full ISR = committed, most durable, slower). Correct per Kafka semantics; acks=all durability after leader failure correctly explained.
- Consumer side: offsets + commit, rewind/replay, retention window + segment drop, independent consumer groups — correct. Delete-after-ack queue (SQS/RabbitMQ: visibility timeout, ack deletes, redeliver, DLQ, no replay) vs retained log (Kafka: kept for retention, read doesn't delete, multi-group replay) correctly contrasted with selection criteria.
- Quizzes: b03 (append-only sequential + segment delete; distractors correctly reject "durable without replication" and "edit mid-log"), b07 (acks=all survives leader death because committed to ISR), b10 (3 independent consumers + 3-day replay → retained log) — every `answer` + `explain_md` correct.
- Mastery: S235 diff1 recall (append-only + segment delete), S236 diff2 scenario (acks=1 lost orders → acks=all, 3-part), S237 diff3 interview "Design Kafka" covering log→partition→replica, acks/ISR, two broker types — matching Mức-3 bar. Levels/rubrics sensible.
- Reuse: explicitly extends sd.async.kafka_log (user-side) into broker-side; no re-teach of offset/consumer-group basics.
- Language: Vietnamese clear; English terms parenthesized.
