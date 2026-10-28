# Review: ml.rag_agents.hybrid_rerank

**Verdict: PASS (clean, publishable).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- Dense/semantic vs sparse/lexical (BM25) strengths/weaknesses correct and symmetric (dense = meaning/synonyms, weak on exact tokens; BM25 = exact match via inverted index, weak on paraphrase).
- Hybrid fusion: **RRF** described correctly — rank-only, `1/(k + rank)` summed per list, k≈60, no score normalization needed; weighted-score fusion correctly flagged as needing normalization. Both current.
- Two-stage retrieve-then-rerank correct: stage-1 bi-encoder/hybrid wide (top-100), stage-2 **cross-encoder** reads (query, passage) jointly → more accurate but slow, only on small candidate set. Never run cross-encoder over whole corpus. All accurate.
- Metrics recall@k, MRR/NDCG and the numeric tradeoff framing (0.62 → 0.78 → 0.88 with p95 40→180ms) are sensible and well presented.

## Quiz / fill items
- b03 (a), b05 (RRF), b08 (a), b10 (a): all `answer` + `explain_md` correct. Distractors target real misconceptions (dense always wins; rerank whole corpus; RRF retrains embeddings).

## Mastery items
- S298 diff1 recall: dense vs BM25 strengths/weaknesses, both directions required. Right level.
- S299 diff2: dense-only system failing on exact codes + ranking — hybrid + rerank + RRF. Matches lesson.
- S300 diff3 interview: matches `mastery_bar_vi` (design BM25+vector+rerank, explain RRF, prove with recall@k + added latency). Rubric requires RRF + cross-encoder role + numeric justification. Right level.
- Mastery items stay within lesson scope.

## Vietnamese + terms
Clear; terms parenthesized (dense/sparse/lexical, BM25, RRF, bi-encoder, cross-encoder, recall@k, MRR/NDCG, p95).

## Minor nit (not a fix)
- b04/b10 state cosine is "bị chặn 0..1". Cosine similarity is formally [-1, 1]; it is effectively ~[0,1] for typical text embeddings. Acceptable simplification in context; does not affect the RRF point (which is that the two score scales differ). Leave as-is.

No must-fix items.
