# Review — ml.system_design.recommendation

**Verdict: PASS (publish-ready).** Accurate, current. No must-fix.

## Reviewed
- `content/lessons/ml/ml.system_design.recommendation.yaml`
- `content/checks_extra/ml.system_design.recommendation.yaml` (S352/S353/S354)

## Findings
- All required elements present:
  - **Candidate gen + ranking** two-stage funnel, explicitly reusing ranking_funnel; retrieval sources run in parallel then merged: collaborative filtering, two-tower + ANN (with negative / hard-negative sampling), co-engagement, fresh/popular (b02/b03). Correct and current.
  - **Multi-objective value model**: weighted combo (example 0.5·P(complete)+0.3·P(like)−1.0·P(report)); weights are a product decision; diversity/freshness/creator fairness; short-vs-long-term clickbait→retention trap with fix (b06). Correct.
  - **Cold start**: users (popularity/onboarding/content-based) and items (content features + exploration) (b08). Correct, both sides.
  - **A/B with long-term holdout**: offline recall@k/NDCG are weak proxies; A/B is the real test; long-term holdout over weeks catches delayed harm (b09/b10/b11). Correct — "offline tốt không bảo đảm online tốt" stated.
- Implicit-feedback labels (watch time, completion, skip, report) correctly flagged as abundant-but-biased (b01).
- Multi-task ranker with shared backbone described accurately (b05).
- Feedback loop / filter bubble callout correct, tied back to exploration/diversity/fairness (b11).
- Quizzes correct: b04=a (scale+latency reason for two stages, refutes "two always better" and "ranker needs no features"), b07=a (clickbait→retention, multi-objective fix), b10 fill=long-term holdout. Explanations sound.
- Mastery: S352 diff1 recall (two stages + why); S353 diff2 scenario (CTR→retention diagnosis, objective fix, reliable eval); S354 diff3 50M-user/20M-item full design matching mastery_bar_vi (two-stage, multi-objective, cold start both sides, A/B + long-term holdout). Rubrics level-appropriate.
- Vietnamese clear; English terms parenthesized.

## Minor (non-blocking)
- None material.
