# Review: sd.archetypes.likes_comments

**Verdict: PASS (clean, publishable).** Independent content review, 2026.

## Technical accuracy & currency
- Hot-counter problem correctly framed: all likes funnel into one row → row-lock contention → write hotspot. Root cause ("ghi dồn một chỗ", not total write volume) stated correctly.
- Sharded counter correct: split into K sub-counters, each like increments a random shard, read = SUM of K shards. Tradeoff (cheaper write, slightly costlier read, masked by cache) accurate.
- Write coalescing / batching correct: buffer increments in Redis/memory, periodic flush, thousands/s → ~1 write/s; durability tradeoff (lose un-flushed increments) honestly noted.
- Duplicate-like prevention correct: unique key `(user_id, post_id)` + idempotent set-state API; counter changes only on real row add/remove. "One person = one like" guaranteed at data layer, independent of the (eventually-consistent) displayed count. This boundary is drawn precisely in b10/S261.
- Eventual consistency of displayed count correctly identified as the enabling condition for cache/shard/coalescing.
- Reuses already-taught concepts (sharding, distributed_cache, idempotency) by reference — no re-teach.

## Quizzes
- b03 (COUNT vs precomputed) ans=b ✓; distractors fair, explain correct.
- b06 (sharded counter mechanism) ans=a ✓; explain correct.
- b07 fill (coalescing/batching) accept-list sensible ✓.
- b09 (retry dedup) ans=b ✓; explain correctly rejects "trust the client".

## Mastery items
- S259 diff1 recall (what is hot counter, why viral jams it): answer_md correct, rubric sensible, right level.
- S260 diff2 score-2 scenario (100k likes/s, fix the write path): 3-part answer correct, rubric keyed to the 3 ideas. Right level.
- S261 diff3 interview: covers storage / dup-prevention / shard+coalesce+cache+eventual-consistency / comment pagination — matches `mastery_bar_vi`. Rubric correctly demands the eventual-consistency-vs-uniqueness boundary.

## Language
Vietnamese clear; English terms parenthesized consistently (hot counter, sharded counter, write coalescing, idempotency, eventual consistency, cursor pagination).

No must-fix items.
