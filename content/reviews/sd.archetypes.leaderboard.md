# Review: sd.archetypes.leaderboard

**Verdict: APPROVE** (no must-fix). Reviewer: independent content pass, 2026-10-27.

## Technical accuracy & currency
- Three core ops (update score, top-N, a user's own rank) + real-time framing correct.
- **Redis ZSET verified**: ZADD O(log n), ZREVRANGE O(log n + N), ZREVRANK O(log n). All complexities correct and current.
- **SQL rank verified**: `COUNT(*) WHERE score > x` is O(n) per query, un-cacheable under continuous updates -> too slow at scale; top-N with an index on score is acceptable (correctly identified as not the bottleneck). Correct.
- Scale: sharded leaderboard + top-N merge (global top-N drawn from per-shard top-N) correct; approximate rank (percentile/buckets) for the long tail, exact rank only for the top — correct.
- Persistence: Redis not source of truth, RDB/AOF snapshot + score_events in durable DB to rebuild — correct. Time-window boards via per-period key + TTL — correct.
- Tie-breaking by encoding time into the score: valid technique; kept conceptual (float64 precision caveat not needed at this level). Acceptable.

## Checks
- Quiz b04 (b, COUNT(*) O(n) vs ZREVRANK O(log n)), b06 fill (ZADD / ZREVRANK), b09 (b, per-week key + TTL) — all answers + explanations correct. b06 explain correctly adds ZREVRANGE for top-N.
- S175 diff1 recall (3 ops + ZSET): correct; rubric sensible.
- S176 diff2 score-2 scenario (SQL rank bottleneck): answer correct, identifies COUNT(*) O(n) + non-cacheable; rubric sensible.
- S177 diff3 interview: matches mastery_bar level 3 (real-time ZSET board, shard by score range when too large, answer a user's rank). Rubric aligns. Good.

## Pedagogy / language
- Reuses prerequisites (caching.patterns, distributed_cache, sql_vs_nosql) by applying; ZSET ops introduced as the archetype's core (appropriate, not re-teaching cache).
- Vietnamese clear; English terms parenthesized consistently.

No corrections required.
