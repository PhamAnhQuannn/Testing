# Review — ml.system_design.fraud_detection

**Verdict: PASS (publish-ready).** Accurate, current, well-scoped. No must-fix.

## Reviewed
- `content/lessons/ml/ml.system_design.fraud_detection.yaml`
- `content/checks_extra/ml.system_design.fraud_detection.yaml` (S340/S341/S342)

## Findings
- Explicitly reuses the framework ("không lặp lại khung đó — ta chỉ áp dụng nó") instead of re-teaching it. Good.
- Special checks all met:
  - Class imbalance → accuracy useless; measures on the rare class: precision/recall @ threshold, PR-AUC (noted more sensitive than ROC-AUC for rare class — correct), precision@k by review capacity, per-category (policy taxonomy, multi-label/multimodal), prevalence-based sampling (b02/b03).
  - Cost-based threshold: minimize (FN × cost_FN) + (FP × cost_FP); $100 vs $5 → lower threshold, favor recall (b03). Correct.
  - Delayed/noisy labels: chargeback ~30–60 days, label-maturity window, reviewer labels early-but-biased (b05). Correct and realistic.
  - Drift/adversarial: frequent retrain, drift monitoring, online/velocity/graph features, keep an instantly-updatable rules tier (b07). Correct.
  - Human-review loop: model triages, reviewer handles gray zone, reviewer labels feed back to training + precision measurement; prioritize queue by risk × value; explainability for reviewers/appeals/audit (b08/b09). Correct.
  - 2026 currency: LLM input/output safety classifiers mentioned (b08). Appropriate.
- Quizzes correct: b04=a, b06=a (fresh data not label-mature → inflated recall), b10 fill=precision@k, b11=a (reviewer role). Distractors are plausible and explanations refute them properly.
- Mastery: S340 diff1 recall (why accuracy fails + 2 alternatives); S341 diff2 scenario (threshold + maturity window + metric); S342 diff3 end-to-end interview matching mastery_bar_vi (cost + per-category metric, delayed labels, drift, reviewer loop). Rubrics name the mandatory pillars correctly.
- Vietnamese clear; English terms parenthesized.

## Minor (non-blocking)
- None material.
