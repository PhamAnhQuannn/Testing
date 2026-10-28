# Review: ml.rag_agents.vector_indexes

**Verdict: PASS (clean, publishable).** Independent content review, 2026-10-27.

## Technical accuracy & currency
- ANN = approximate (trades a little recall for large speedup); flat search ~O(N·d) correct.
  - b01 math: 10M × 768 ≈ 7.68 billion multiply-adds ("7-8 tỉ") — correct.
- Metrics cosine / dot / L2 correct; normalized vectors → cosine = dot product, and rank order matches L2 — correct.
- **HNSW**: multi-layer graph, efSearch is the search-time knob (larger = higher recall, slower), M/efConstruction build knobs, best recall/latency but more RAM — all correct.
- **IVF**: k-means clusters, nprobe = #cells probed (larger = higher recall, slower) — correct.
- **PQ**: splits vector into segments → short codes via codebook, compresses RAM, lowers recall; IVF-PQ for billion-scale — correct.
  - b07 math: 10M × 768 × 4 bytes ≈ 30 GB — correct.
  - S297 math: 200M × 1024 × 4 bytes ≈ 800 GB — correct.
- recall-latency-memory tradeoff, filtered search (pre- vs post-filter), vector DBs (pgvector/FAISS/Milvus/Qdrant/Weaviate/Pinecone) accurate and current.

## Quiz / fill items
- b04 (a), b08 (a), b11 (nprobe): all `answer` + `explain_md` correct. b08 distractors precisely target the real misconceptions (PQ raises recall — false; nprobe is IVF not HNSW).

## Mastery items
- S295 diff1 recall: flat cost + ANN recall tradeoff. Right level.
- S296 diff2: HNSW low-recall scenario — efSearch direction, latency tradeoff, measure vs flat. Matches lesson.
- S297 diff3 interview: 200M/1024-dim, recall@10 ≥ 0.95, p95 < 30ms, limited RAM — matches `mastery_bar_vi` (explain HNSW/IVF/PQ, tune efSearch/nprobe, choose DB with justification). Excellent, correctly reasons RAM as the binding constraint → IVF-PQ. Right level.
- Mastery items stay within lesson scope.

## Vietnamese + terms
Clear; terms parenthesized (ANN, recall@k, efSearch, nprobe, PQ, IVF-PQ, pre/post-filter). Minor: objective line 10 duplicates the "Mức 3" bar as an objective — stylistic only, not an error.

No must-fix items.
