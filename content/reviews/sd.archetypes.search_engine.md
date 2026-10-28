# Review: sd.archetypes.search_engine

**Verdict: PASS** (independent content review, 2026). No must-fix.

## Technical accuracy
- Inverted index = term → posting list (docs containing term); open the term's list instead of scanning all docs. Correct, reuses search_indexing.
- Index is a separate system from the source DB (source DB optimizes writes + primary-key lookups, not fast full-text at scale). Indexing pipeline listens to source-DB changes via **CDC (Change Data Capture)**, tokenizes/normalizes, updates index async → **near-real-time**, eventual lag of seconds. Correct, matches the accepted freshness-lag constraint.
- **Scatter-gather**: coordinator scatters the query to every shard; each shard ranks locally and returns **top-k**; coordinator merges + re-ranks. Tail latency (wait for slowest shard) handled with timeout/partial results. Correct, reuses sharding.
- **Document- vs term-partitioning** (DDIA-aligned):
  - Document-partitioning: each shard holds all terms for a doc subset; every query hits **every** shard; simple indexing (one doc → one shard), even load, no hot term — correctly stated as the default and natural fit for scatter-gather.
  - Term-partitioning: each shard holds a term subset for all docs; a query hits only shards holding its terms (fewer shards), but suffers **hot term** skew and hard rebuild (one doc's many terms span many shards). Correct.
- Replica-per-shard for read throughput + fault tolerance; BM25 (term frequency + inverse document rarity) + signals for ranking; local ranking uses same formula so top-k is mergeable. Correct.

## Quizzes / mastery
- b03 separate index = a correct (b "strong consistency" false, c "smaller/cheaper" false); b05 top-k + re-rank = a correct (b "full replica" / c "coordinator just forwards" false); b07 tip = default doc-partitioning; b08 doc-partitioning default = a correct (b/c reversed/false); b10 fill CDC + BM25 correct.
- S220 (diff1): inverted index + why separate + why near-real-time — recall, right level.
- S221 (diff2): 100M products, 4-part scatter-gather query path incl. tail latency + timeout. Right level.
- S222 (diff3 interview): source DB → pipeline (CDC) → sharded index → scatter-gather → doc- vs term-partitioning + default justification. Matches mastery_bar. Rubrics sensible.

## Reuse (no re-teach)
Explicitly cites sd.data.search_indexing and sd.data.sharding (both exist) without re-teaching. Good.

## Language
Clear Vietnamese; English terms parenthesized (inverted index, posting list, CDC, scatter-gather, top-k, tail latency, document/term-partitioning, hot term, BM25, replica). No issues.
