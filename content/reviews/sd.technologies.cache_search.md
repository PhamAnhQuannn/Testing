# Review: sd.technologies.cache_search

**Verdict: PASS (clean, ready to publish).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Redis = in-memory data-structure store; good for cache, session, rate limit (atomic increment + TTL), leaderboard (sorted set), ephemeral data. Correct.
- Redis limits stated correctly: **memory-bound** (must fit in RAM, bad for large/cold data) and **volatile / not a system of record** (RDB/AOF can still lose the last few seconds on crash; treat as rebuildable from the source DB). Accurate.
- Elasticsearch/OpenSearch = inverted-index search/analytics engine; good for full-text/fuzzy, multi-filter, aggregation, relevance ranking. Correct.
- ES limits stated correctly: **near-real-time** (default ~1s refresh → index freshness lag) and **not a system of record** (secondary index synced from source DB via CDC; reindex is expensive). Accurate and current.

## Quizzes
- b04 (per-minute rate limiter → Redis): answer `a` correct; explain correctly notes ES is NRT/heavy and source DB is slower for hot counters.
- b07 (50M-item autocomplete, fuzzy + filter → Elasticsearch): answer `b` correct; correctly rejects Redis (key lookup only, RAM cost) and SQL `LIKE '%...%'` (no index, full scan).
- b08 fill: accepts "system of record" / "source of truth" — both correct.

## Mastery items
- S154 diff1 recall (what each system is + one use each) — right level.
- S155 diff2 scenario (both misuses: ES as SoR, Redis as 50M-item store) — score-2, rubric sensible.
- S156 diff3 interview (A autocomplete=ES, B rate-limit=Redis, C leaderboard=Redis, each + 1-2 reqs + 1 limit) — matches mastery_bar_vi (Redis/ES selection with memory / index-freshness limits).
- Items test only taught ideas; Vietnamese clear, English parenthesized.

No must-fix items.
