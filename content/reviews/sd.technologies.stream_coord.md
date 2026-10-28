# Review: sd.technologies.stream_coord

**Verdict: PASS (clean, ready to publish).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Kafka = partitioned, durable, replayable log; consumer groups read independently by offset; time-based retention; high throughput via partitioning + sequential writes. Correct.
- **"Kafka is not a task queue"** stated correctly: no per-message ack, no visibility timeout, no natural per-message delay/retry; progress is a linear per-partition offset. Use SQS/RabbitMQ for work-queue semantics. Accurate.
- Flink = true streaming, low latency, stateful, event-time with windows/watermarks (fraud in seconds). Spark = batch + micro-batch, high throughput, reprocessing/ETL/reporting, higher latency. Correct distinction.
- ZooKeeper/etcd = consensus-based (ZAB/Raft) coordination: config, leader election, service discovery, locks; hold small strongly-consistent metadata; etcd backs Kubernetes state. Correct; "don't put large data in them (every write replicates via consensus)" is right.

## Quizzes
- b04 (per-order email → SQS/RabbitMQ): answer `b` correct; `a` correctly rejected (Kafka lacks ack/visibility-timeout/per-message delete).
- b06 (card fraud in seconds, stateful → Flink): answer `b` correct; batch too slow, Kafka alone doesn't compute windows.
- b09 fill (etcd; replicate/nhân bản): accept lists fine.
- b10 (Kafka vs etcd/ZooKeeper roles don't swap): answer `a` correct.

## Mastery items
- S157 diff1 recall (Kafka use + why not a task queue) — right level.
- S158 diff2 scenario (per-order email: rebut "we already have Kafka") — score-2, rubric sensible.
- S159 diff3 interview (a→Kafka, b→Flink, c→Spark, d→etcd/ZooKeeper, each + requirement reason + 1 limit incl "Kafka not a task queue") — matches mastery_bar_vi.
- Items test only taught ideas; Vietnamese clear, English parenthesized.

No must-fix items.
