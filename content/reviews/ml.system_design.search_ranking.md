# Review: ml.system_design.search_ranking

**Verdict: PASS — no must-fix. Technically accurate, currency OK for 2026, ready to publish.**

Reviewer: independent content review (AI-engineer concept track). Date: 2026-10-27.

## Technical accuracy & currency
- 4-tier funnel is correct and current: query understanding → hybrid retrieval → LTR → rerank (cross-encoder on top-k). Matches the special-accuracy checklist exactly.
- Hybrid = BM25 on inverted index + dense/ANN (HNSW, IVF-PQ), fused with RRF. Correct.
- Labels from click logs with position-bias handling (skip-click, click model / IPW, dwell/long-click, pogo-sticking) plus a small rater gold set. Correct and well-framed.
- Evaluation: offline NDCG/MRR + recall@k, online A/B + interleaving as final evidence. Correct; interleaving noted as more sensitive / less traffic — accurate.

## Quizzes (answers + explanations)
- b04 (hybrid, ans a), b08 (skip-click + long-click → pairwise, ans a), b10 fill (position bias), b11 (run A/B before 100% rollout, ans a): all correct, distractors are genuinely wrong for the stated reasons.

## Mastery items
- S355 diff1 recall (name 4 tiers + two retrieval types): right level, answer/rubric correct.
- S356 diff2 score-2 scenario (R1/R2 skipped, R3 long-click → debias → pairwise): right level, answer correct, rubric sensible (core = position-bias debias).
- S357 diff3 interview (end-to-end e-commerce ranker): matches mastery_bar_vi ("thiết kế search ranker end-to-end với cách tạo nhãn từ click, chọn index, rerank và cách đánh giá"). Rubric aligns.

## Prior-concept reuse & language
- Explicitly builds on ranking_funnel and hybrid_rerank without re-teaching. Vietnamese clear; English terms parenthesized consistently (learning to rank, cross-encoder, RRF, IPW, NDCG/MRR, recall@k).
