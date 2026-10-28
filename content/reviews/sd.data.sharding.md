# Review: sd.data.sharding (independent reviewer pass)

**Verdict: OK** (no must-fix; clean)

11 blocks; graded: b03 (mcq), b05 (mcq), b08 (mcq). mastery_check l1 [S052], l2 [S053], l3 [S054].
mastery_bar_vi: "chọn shard key hợp lý, xử lý hot shard và resharding, nêu hậu quả xuyên shard" — S054 covers all.

## Technical accuracy (verified)
- Vertical (by column) vs horizontal/sharding (by row, only way to scale writes) correct.
- Three strategies correct: range (good range scan, skew/hot on newest), hash (even spread, breaks range queries), directory/lookup (flexible, extra lookup tier / SPOF if not replicated+cached).
- Shard-key criteria correct: even spread (high cardinality), match hot query (one query → one shard), avoid cross-shard. `country` as bad key, `conversation_id` as good chat key — correct, consistent with sql_vs_nosql chat example.
- Hot shard (skewed traffic though rows even) + fixes (isolate hot key / replica / cache / key splitting with suffix) correct.
- Resharding: `hash % n` moves nearly all keys when n changes; mitigations over-provision logical partitions + consistent hashing. Correct; forward-reference to consistent_hashing lesson consistent (and that lesson is the prereq-chained next topic).
- Cross-shard cost (scatter-gather aggregate, cross-shard join, distributed txn/2PC → design to avoid) correct.

## Quiz / mastery correctness
- b03 [b] range for time-range queries + hot-newest-shard risk: correct; (a)/(c) refuted correctly.
- b05 [b] `conversation_id` shard key: correct; (a) even-but-cross-shard, (c) country-skew refuted correctly.
- b08 [b] `hash % n` moves ~all keys on reshard: correct; (a) hash speed, (c) range-irrelevant refuted correctly.
- S052 (L1 recall): vertical vs horizontal + 3 strategies. Sensible.
- S053 (L2 gate): shard `orders` — key + even/match justification, range vs hash trade, one cross-shard query. Good gate.
- S054 (L3 interview): shard `posts` — key justification, hot shard (≥2 fixes), resharding pain + mitigation, cross-shard consequences. Matches mastery_bar; answers correct.

## Coverage discipline
Mastery items test only taught ideas. No leakage.

## Cross-lesson consistency
Resharding/consistent-hashing overlap with sd.data.consistent_hashing is consistent: both say `hash % n` reshuffles nearly all keys, consistent hashing moves only a small fraction. No contradiction.

## Language
Vietnamese clear; English terms parenthesised (partitioning, sharding, shard/partition key, range/hash/directory, hot shard, resharding/rebalancing, scatter-gather, cross-shard, 2PC). Good.

## Findings
None blocking. Accurate and interview-correct.
