# Review — ml.system_design.ads_ctr_auction

**Verdict: PASS (publish-ready).** Accurate, current, and the quantitative claims check out. No must-fix.

## Reviewed
- `content/lessons/ml/ml.system_design.ads_ctr_auction.yaml`
- `content/checks_extra/ml.system_design.ads_ctr_auction.yaml` (S349/S350/S351)

## Verified numbers / formulas
- **eCPM = bid × pCTR × 1000** (expected revenue per 1000 impressions); rank score = bid × pCTR (b01/b03). Correct.
- **Auction example** (b03): A(bid 3, pCTR 0.02)=0.06 vs B(bid 1, pCTR 0.07)=0.07 → B wins; inflate A's pCTR to 0.04 → 0.12 → A wins wrongly. Arithmetic correct; cleanly shows calibration changes ranking *across different bids*.
- **Negative-downsampling correction** (b07): p = p'·w / (p'·w + 1 − p'). Derivation sound (true_odds = sampled_odds × w, keeping fraction w of negatives). Worked example w=0.1, p'=0.2 → 0.02/0.82 ≈ 0.024 is correct, and p < p' as expected (downsampling inflates predicted CTR). ✓
- Subtopics.json concept example "bid 2 USD, P=0.05 → 0.10/impression" also correct.

## Findings
- Calibration is the spine and is defined correctly (predicted 2% ⇒ ~2% actual). **AUC-alone-insufficient** nailed: AUC is invariant to monotonic squashing, so two equal-AUC models can differ in money/pacing (b04 callout, b05 quiz). This is the key required point.
- Measurement: reliability diagram + ECE (weighted mean |pred − actual| across bins), fit on held-out (b06). Post-hoc fixes: Platt scaling (few params) vs isotonic regression (non-decreasing step fn, needs more data) — both described accurately.
- Pipeline reuses the funnel (candidate retrieval → score pCTR → auction); sparse/categorical features via hashing + embeddings; online learning for scale/freshness (b02). Current for 2026.
- **Delayed conversions** (b09/b10): CVR labels arrive hours–days later; early labeling creates false negatives → CVR depressed + miscalibrated; fix = attribution window and/or delayed-feedback modeling; CVR also needs calibration. Correct.
- Quizzes correct: b05=a, b08 fill=ECE, b10=a. Explanations refute distractors.
- Mastery: S349 diff1 recall (bid×pCTR + calibration definition); S350 diff2 scenario (AUC-high-but-budget-burns → calibration, measure+fix, downsampling cause); S351 diff3 full pipeline matching mastery_bar_vi. Rubrics level-appropriate and demand the calibration-for-auction pillar.
- Vietnamese clear; English terms parenthesized.

## Minor (non-blocking)
- None material.
