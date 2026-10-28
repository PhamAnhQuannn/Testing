# Review: sd.fundamentals.cap_consistency (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

11 blocks; graded: b05 (mcq), b07 (fill), b09 (mcq). mastery_check l1 [S007], l2 [S008], l3 [S009].
mastery_bar_vi: "phát biểu đúng CAP (đứt mạng -> chọn đúng hoặc sống), chọn mạnh/cuối cùng cho từng loại dữ liệu, nêu ví dụ kho CP/AP" — S009 covers all three.

## Technical accuracy (verified)
- CAP stated the correct 2026 way: NOT "pick 2 of 3"; explicitly "during a partition, choose C or A; no partition -> both" (b04, b05, b10, summary, S007, S009). This is exactly the required framing.
- Partition defined correctly as a network fault (nodes alive but can't communicate), always possible on a real distributed system. P mandatory. Correct.
- PACELC: "P -> A or C; E(lse) -> L or C" (Abadi). Else-branch (latency vs consistency even with no partition, via wait-for-replicas) explained correctly (b06, b07, S009). Correct.
- Strong vs eventual definitions correct; per-data-type mapping (balance/inventory/booking -> strong; likes/views/feed -> eventual) correct.
- CP stores etcd, ZooKeeper (consensus-based, config/leader election) correct. AP stores Cassandra, DynamoDB correct, with the accurate caveat that both offer tunable/per-query consistency so not "absolutely AP".

## Quiz / mastery correctness
- b05 answer [b] correct; (a) "2 of 3 at all times" and (c) "partition avoidable" correctly refuted.
- b07 fill: Latency, Consistency — correct; accept lists cover EN + VN forms.
- b09 answer [a] (balance strong, likes eventual) correct; (b) reversed, (c) over-strong correctly refuted.
- S007 (L1): names 3 letters + "partition -> choose C or A"; rubric correctly fails "2 of 3 at all times".
- S008 (L2 gate): per-data-type choice + reasons; genuine scenario application, rubric requires correct reasons. Good gate.
- S009 (L3 interview): precise CAP statement + PACELC else-branch + one CP + one AP example; forbids "2 of 3". Matches mastery_bar_vi. Answer correct.

## Coverage discipline
Mastery items test only taught ideas (CAP statement, PACELC else, strong/eventual per data type, CP/AP examples). No leakage. Beginner callout (b03) sensibly scopes strong-vs-eventual for freshers.

## Language
Vietnamese clear; English terms parenthesised on first use (partition, consistency, availability, CAP, PACELC, strong/eventual, CP/AP). Good.

## Findings
None blocking. Content is accurate and interview-correct.
