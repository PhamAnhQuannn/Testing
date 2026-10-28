# Review: sd.data.replication (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

12 blocks; graded: b03 (mcq), b05 (mcq), b07 (mcq), b09 (mcq). mastery_check l1 [S049], l2 [S050], l3 [S051].
mastery_bar_vi: "so sánh sync/async, giải thích lag, failover, split-brain, chọn cấu hình cho yêu cầu cụ thể" — S051 covers all.

## Technical accuracy (verified)
- Three reasons (availability, durability, read scaling) correct; "replication ≠ backup" (a bad delete propagates) correct.
- Leader-follower correct: only leader takes writes; read replicas scale reads not writes; multi-leader/leaderless noted with write-conflict caveat. Correct.
- Sync vs async durability-vs-latency trade-off correct; semi-sync as the middle point correct.
- Replication lag → stale reads; read-after-write / read-your-writes fixes (read own data from leader; track write position; monotonic reads by pinning to one replica) all correct.
- Failover, split-brain, quorum/majority (only one majority at a time) and fencing token/STONITH correct. Failover trade-offs (async may lose writes; timeout too short/long) correct.
- Builds correctly on sd.fundamentals.cap_consistency (b01 reference; PACELC in b04). Consistent with that lesson.

## Quiz / mastery correctness
- b03 [b] read replicas scale reads only: correct.
- b05 [b] async + leader dies pre-replication → write can be lost despite ack: correct; (a)/(c) refuted correctly.
- b07 [a] lag → read-after-write fix: correct; (b) failover, (c) backup correctly refuted.
- b09 [a] only one majority can exist → no two valid leaders: correct; (b)/(c) (conflating quorum with sync/no-lag) refuted correctly.
- S049 (L1 recall): who takes writes, replicas scale reads. Sensible.
- S050 (L2 gate): stale-name scenario — lag, consistency-not-durability, a fix. Good gate.
- S051 (L3 interview): sync vs async + lag/failover/split-brain + quorum/fencing + config choice (bank sync / likes async). Matches mastery_bar; answers correct.

## Coverage discipline
Mastery items test only taught ideas. Minor: b04 labels the sync/async durability-vs-latency trade as "PACELC at a concrete level"; PACELC's else-branch is strictly latency-vs-consistency — framing is slightly loose but defensible (sync also affects read consistency). Not blocking.

## Language
Vietnamese clear; English terms parenthesised (replication, leader/follower, sync/async, replication lag, read-after-write, failover, split-brain, quorum, fencing token). Good.

## Findings
None blocking. Accurate and interview-correct.
