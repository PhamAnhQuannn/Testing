# Review: sd.framework.deep_dive_tradeoffs (independent reviewer pass)

**Verdict: OK** (no must-fix)

11 blocks; graded: b03 (mcq), b06 (fill), b07 (mcq), b09 (mcq). mastery_check l1[S040] l2[S041] l3[S042].
mastery_bar_vi: "tự tìm điểm nghẽn, nêu 2 phương án A/B, chọn một có lý do, trả lời 'nếu X chết'" — S042 matches.

## Technical accuracy
- Bottleneck taxonomy: single write DB, hot key/partition, fan-out, SPOF — correct and complete for this level.
- A/B trade-off template + classic axes (latency vs consistency, cost vs complexity, read-optimized vs write-optimized). Correct.
- Fan-out-on-write vs fan-out-on-read, hybrid for celebrities — canonical feed design, current for 2026.
- Failure answer = SPOF → replication/failover (primary+standby, async writes may be lost), + graceful degradation; cache stampede risk when cache dies. All correct.

## Quiz / mastery correctness
- b03 [b] primary = write bottleneck/SPOF — correct; (a) stateless-LB and (c) "app servers" refuted.
- b06 fill: fan-out / read (fan-out-on-write, fan-out-on-read) — correct.
- b07 [b] choose cache with reason tied to requirement — correct; (a) "always exact" and (c) refuse-to-choose correctly refuted (the "choice + reason is what's graded" point is the lesson's core).
- b09 [b] cache dies → read DB directly (degrade) + watch stampede — correct; (a)/(c) refuted.
- S040 (L1): bottleneck def + 2 types; rubric sensible.
- S041 (L2 gate): news feed — bottleneck + fan-out-on-write/read A/B with pro/con + trade-off axis. Correct.
- S042 (L3): URL shortener — full 4-step deep dive (bottleneck, A/B, choose+why tied to read-heavy, "if cache dies"). Matches bar + lesson's b10 4-step frame.

## Consistency
Step 6 of the pipeline; opens from the HLD diagram (write-to-primary bottleneck carried over from hld_diagram/scalability). "Choose based on requirements locked at the start" ties back to the requirements subtopic. URL-shortener and read-heavy examples consistent across the set.

## Coverage discipline
All mastery items test only taught ideas (bottleneck types, A/B template, fan-out, cache stampede, failover, graceful degradation). No leakage.

## Language
Vietnamese clear; English terms parenthesized (bottleneck, hot key/partition, fan-out, SPOF, trade-off, replication/failover, graceful degradation, cache stampede). Good.
