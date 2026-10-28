# Review — ml.system_design.ranking_funnel

**Verdict: PASS (publish-ready).** Accurate, current. No must-fix.

## Reviewed
- `content/lessons/ml/ml.system_design.ranking_funnel.yaml`
- `content/checks_extra/ml.system_design.ranking_funnel.yaml` (S346/S347/S348)

## Findings
- Required structure present: retrieval/candidate generation → (optional) pre-ranking → heavy ranking → re-ranking, each with a latency budget as the *reason* the funnel exists (b01–b03). Opposite roles stated correctly: retrieval = cheap + high recall; ranker = expensive + high precision on a small set. Interview callout gives concrete numbers (~1e8 → 1e3 → 1e1, retrieval ~10ms / ranking ~50ms) — exactly the expected framing.
- Retrieval techniques current: ANN over two-tower embeddings, co-occurrence/heuristics (b02). Re-ranking covers diversity, dedup, business rules (b03).
- Three pitfalls + fixes all covered correctly:
  - **Position bias**: high-position clicks biased → model mimics old ranking; fix = position feature (set to constant at serving) or IPS weight 1/P(seen) (b06). Correct.
  - **Cold start**: new user/item lack history; fix = content features + exploration (b08).
  - **Feedback loop / exposure bias**: trains on self-generated impression logs → hot-gets-hotter; fix = exploration (bandit/ε-greedy) + randomization (b08). Correct; root cause (missing observations) well explained.
- Quizzes correct: b05=a, b07=a (position bias fix), b09=a (feedback loop vs the overfitting/position-bias distractors), b10 fill=bandit. Explanations refute distractors properly.
- Mastery: S346 diff1 recall (tiers in order + latency reason); S347 diff2 scenario (identify 2 traps + fixes); S348 diff3 100M-item interview matching mastery_bar_vi (funnel + latency budget AND all three traps + fixes). Rubrics level-appropriate.
- Vietnamese clear; English terms parenthesized.

## Minor (non-blocking)
- Subtopic `name_vi` in subtopics.json is "Phễu retrieval-ranking, bẫy xếp hạng và CTR quảng cáo" and its key_concepts list CTR/CVR-calibration/auction/downsampling — but this lesson (correctly) offloads CTR/auction to the separate `ads_ctr_auction` subtopic and does not cover them. The binding `mastery_bar_vi` does NOT require CTR, and the lesson fully satisfies that bar, so this is a tree-metadata/scope artifact, not a lesson defect. No action needed on the lesson.
