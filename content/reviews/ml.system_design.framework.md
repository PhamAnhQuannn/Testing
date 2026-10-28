# Review — ml.system_design.framework

**Verdict: PASS (publish-ready).** Technically accurate and current for 2026. No must-fix.

## Reviewed
- `content/lessons/ml/ml.system_design.framework.yaml`
- `content/checks_extra/ml.system_design.framework.yaml` (S337 diff1 / S338 diff2 / S339 diff3)

## Findings
- Ordered steps correct: clarify → data/features → model (baseline first) → evaluation (offline time-aware + online A/B) → serving → monitoring/retraining. Metric+label explicitly framed as the highest-leverage step (b01 time-management tip, b04 interview callout). Matches the required canonical order.
- Metric two-tier (offline model metric vs online/business) + guardrail metric correct and clearly separated (b02).
- Label treatment solid: source, delayed, noisy/biased, observation window + prediction horizon (b03).
- Quizzes correct: b05 answer=a (metric+label highest leverage for fraud), b08 answer=a (offline-great/online-dead = leakage or train-serving skew; point-in-time + time split), b11 fill = drift / retrain. Explanations sound.
- QPS estimate (b09): 10M req/day ÷ 86,400 ≈ 115 avg, peak → ~500. Arithmetic correct, right order of magnitude.
- Trade-offs named (latency vs accuracy, fresh vs stable, batch vs online) — what interviewers want.
- Mastery items: S337 (recall 6 steps + why clarify first) is correct diff1 recall; S338 is a proper score-2 scenario (churn clarify → problem/metric/label); S339 is a full 45-min interview walk-through matching mastery_bar_vi. S339 QPS (50M ÷ 86,400 ≈ 580, peak 2-3k) correct. Rubrics sensible and level-appropriate.
- Vietnamese clear; English terms parenthesized throughout (clarify, leakage, point-in-time, guardrail, A/B, drift...).

## Minor (non-blocking)
- None material.
