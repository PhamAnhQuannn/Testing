# Review: ml.system_design.multimodal_retrieval

**Verdict: PASS — no must-fix. Technically accurate, currency OK for 2026, ready to publish.**

Reviewer: independent content review (AI-engineer concept track). Date: 2026-10-27.

## Technical accuracy & currency
- Joint/shared embedding space via CLIP-style dual encoder + contrastive loss; text→image search = embed query then ANN nearest-neighbor. Correct, matches checklist.
- Offline (batch encode + index) vs online (embed query + ANN, optional re-rank) split: correct.
- Video: frame/shot sampling + temporal (mean) pooling, or per-segment indexing for localization. Correct and appropriately nuanced.
- ANN at billion scale: HNSW (fast, RAM-heavy) vs IVF-PQ (compressed) + sharding/fan-out-merge; framed as recall ↔ latency ↔ memory/cost tradeoff. Correct.
- Near-dup: pHash (Hamming) for near-identical + embedding-threshold for hard near-dupes (crop, logo, re-encode). Matches checklist. Good contrast vs cryptographic hash.
- Eval: recall@k / precision@k on labeled set (caption-as-query trick when no user labels), human eval, modality gap + safe-content note. Correct.

## Quizzes
- b03 (why CLIP enables text search, ans a), b06 (IVF-PQ + sharding at 1B, ans a), b09 (layered pHash + embedding, ans a), b11 fill (recall@k): all correct; distractors (cryptographic hash useless for near-dup, brute-force too slow) are sound.

## Mastery items
- S358 diff1 recall (joint embedding + search = nearest neighbor): right level.
- S359 diff2 (video search design: offline/online, pooling, index choice): right level, correct.
- S360 diff3 interview (billion-scale search + near-dup detection + eval): matches mastery_bar_vi. Rubric aligns (three pillars).

## Prior-concept reuse & language
- Reuses search_ranking and vector_indexes (ANN types) without re-teaching. Vietnamese clear; English terms parenthesized (contrastive loss, HNSW, IVF-PQ, perceptual hash, modality gap, recall@k).
