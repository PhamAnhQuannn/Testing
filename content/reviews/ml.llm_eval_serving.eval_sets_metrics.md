# Review: ml.llm_eval_serving.eval_sets_metrics

**Reviewer:** independent content reviewer (AI-engineer track)
**Date:** 2026-10-27
**Verdict: PASS — no must-fix.** Accurate, current (2026), well-pitched; quizzes and mastery items all correct.

## Technical accuracy & currency
- Eval set built from real production traffic + failure cases, versioned, small-but-useful (20-50), living set — all correct and current.
- Task-specific metrics correct: classification → accuracy/F1; extraction → exact-match/F1-per-field; RAG retrieval → recall@k/precision@k; RAG generation → groundedness/answer relevance (judge or human); code → pass@k (≥1 of k passes tests); reference text → BLEU/ROUGE.
- Metric limits correct: exact-match too strict for free text (needs normalization); BLEU/ROUGE count n-gram overlap → miss meaning, weak proxy; BERTScore (embedding) better but imperfect; single aggregate hides slices → slice + error analysis. All matches the SPECIAL checks.
- Offline (pre-ship, CI regression) vs online distinction correct.

## Quizzes
- b03 answer [a] correct (representative + failure cases + versioned); distractors correctly refuted.
- b06 answer [a] recall@k for retrieval correct; BLEU/pass@k correctly rejected.
- b10 fill recall@k with sensible accept list; explain correct (precision@k = inverse).

## Mastery items
- S310 (diff1 recall): defines eval set + one reason vibe check fails — correct, right level; rubric sensible.
- S311 (diff2 score-2 scenario): invoice extraction; exact-match/F1 + real-data source + normalize limit — all taught in lesson (b04/b07); rubric sensible.
- S312 (diff3 interview): RAG, separates retrieval (recall@k) vs generation (groundedness/answer relevance via judge), limits + offline gate + online — matches `mastery_bar_vi` ("xây eval set, chọn metric, giải thích giới hạn"). Only tests ideas the lesson teaches.

## Language
Vietnamese clear; English terms parenthesized consistently (golden set, exact-match, recall@k, pass@k, groundedness, regression suite).
